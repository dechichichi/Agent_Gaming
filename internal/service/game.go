package service

import (
	"agent-gaming/internal/model"
	"context"
	"encoding/json"
	"fmt"
	"sync"
	"time"

	"github.com/go-redis/redis/v8"
	"gorm.io/gorm"
)

// GameService 游戏服务
type GameService struct {
	db    *gorm.DB
	redis *redis.Client
	// 用于异步处理的通道
	eventChan chan *model.UserEvent
	// 工作池
	workerPool chan struct{}
	// 互斥锁
	mu sync.RWMutex
}

// NewGameService 创建游戏服务
func NewGameService(db *gorm.DB, redis *redis.Client) *GameService {
	service := &GameService{
		db:         db,
		redis:      redis,
		eventChan:  make(chan *model.UserEvent, 1000), // 缓冲通道
		workerPool: make(chan struct{}, 10),           // 10个工作协程
	}

	// 启动异步事件处理器
	go service.startEventProcessor()

	return service
}

// RecordEventAsync 异步记录事件
func (s *GameService) RecordEventAsync(event *model.UserEvent) error {
	select {
	case s.eventChan <- event:
		return nil
	default:
		// 通道满了，直接写入数据库
		return s.db.Create(event).Error
	}
}

// startEventProcessor 启动事件处理器
func (s *GameService) startEventProcessor() {
	for event := range s.eventChan {
		s.workerPool <- struct{}{} // 获取工作槽
		go func(e *model.UserEvent) {
			defer func() { <-s.workerPool }() // 释放工作槽
			s.processEvent(e)
		}(event)
	}
}

// processEvent 处理单个事件
func (s *GameService) processEvent(event *model.UserEvent) {
	// 写入数据库
	if err := s.db.Create(event).Error; err != nil {
		fmt.Printf("Failed to save event: %v\n", err)
		return
	}

	// 更新用户统计缓存
	s.updateUserStatsCache(event.UserID)
}

// GetUserEvents 获取用户事件
func (s *GameService) GetUserEvents(userID string, limit int) ([]model.UserEvent, error) {
	var events []model.UserEvent

	// 使用读写锁保护并发访问
	s.mu.RLock()
	defer s.mu.RUnlock()

	err := s.db.Where("user_id = ?", userID).
		Order("event_time DESC").
		Limit(limit).
		Find(&events).Error

	return events, err
}

// GetUserAnalytics 获取用户分析数据
func (s *GameService) GetUserAnalytics(userID, startDate, endDate string) (map[string]interface{}, error) {
	analytics := make(map[string]interface{})

	// 获取事件统计
	var eventStats []struct {
		EventName string `json:"event_name"`
		Count     int64  `json:"count"`
	}

	query := s.db.Model(&model.UserEvent{}).Select("event_name, COUNT(*) as count").
		Where("user_id = ?", userID)

	if startDate != "" {
		query = query.Where("part_date >= ?", startDate)
	}
	if endDate != "" {
		query = query.Where("part_date <= ?", endDate)
	}

	err := query.Group("event_name").Find(&eventStats).Error
	if err != nil {
		return nil, err
	}

	analytics["event_stats"] = eventStats

	// 获取时间分布
	var timeDistribution []struct {
		Hour  int   `json:"hour"`
		Count int64 `json:"count"`
	}

	err = s.db.Model(&model.UserEvent{}).
		Select("HOUR(FROM_UNIXTIME(event_time)) as hour, COUNT(*) as count").
		Where("user_id = ?", userID).
		Group("hour").
		Order("hour").
		Find(&timeDistribution).Error

	if err != nil {
		return nil, err
	}

	analytics["time_distribution"] = timeDistribution

	// 获取活跃度趋势
	var activityTrend []struct {
		Date  string `json:"date"`
		Count int64  `json:"count"`
	}

	err = s.db.Model(&model.UserEvent{}).
		Select("part_date as date, COUNT(*) as count").
		Where("user_id = ?", userID).
		Group("part_date").
		Order("part_date").
		Find(&activityTrend).Error

	if err != nil {
		return nil, err
	}

	analytics["activity_trend"] = activityTrend

	return analytics, nil
}

// GetUserStats 获取用户统计
func (s *GameService) GetUserStats(userID string) (map[string]interface{}, error) {
	stats := make(map[string]interface{})

	// 获取总事件数
	var totalEvents int64
	err := s.db.Model(&model.UserEvent{}).Where("user_id = ?", userID).Count(&totalEvents).Error
	if err != nil {
		return nil, err
	}
	stats["total_events"] = totalEvents

	// 获取事件类型数
	var eventTypes int64
	err = s.db.Model(&model.UserEvent{}).Where("user_id = ?", userID).Distinct("event_name").Count(&eventTypes).Error
	if err != nil {
		return nil, err
	}
	stats["event_types"] = eventTypes

	// 获取首次和最后活动时间
	var firstEvent, lastEvent model.UserEvent
	err = s.db.Where("user_id = ?", userID).Order("event_time ASC").First(&firstEvent).Error
	if err == nil {
		stats["first_activity"] = firstEvent.EventTime
	}

	err = s.db.Where("user_id = ?", userID).Order("event_time DESC").First(&lastEvent).Error
	if err == nil {
		stats["last_activity"] = lastEvent.EventTime
	}

	// 计算活跃天数
	var activeDays int64
	err = s.db.Model(&model.UserEvent{}).Where("user_id = ?", userID).Distinct("part_date").Count(&activeDays).Error
	if err != nil {
		return nil, err
	}
	stats["active_days"] = activeDays

	return stats, nil
}

// BatchRecordEvents 批量记录事件
func (s *GameService) BatchRecordEvents(events []EventRequest) error {
	if len(events) == 0 {
		return nil
	}

	// 转换为模型
	modelEvents := make([]*model.UserEvent, len(events))
	for i, event := range events {
		modelEvents[i] = &model.UserEvent{
			ID:        generateUUID(),
			UserID:    event.UserID,
			EventName: event.EventName,
			EventTime: event.EventTime,
			EventInfo: string(event.EventInfo),
			PartDate:  event.PartDate,
		}
	}

	// 批量插入
	return s.db.CreateInBatches(modelEvents, 100).Error
}

// updateUserStatsCache 更新用户统计缓存
func (s *GameService) updateUserStatsCache(userID string) {
	ctx := context.Background()
	cacheKey := fmt.Sprintf("user_stats:%s", userID)

	// 删除缓存，下次查询时重新计算
	s.redis.Del(ctx, cacheKey)
}

// generateUUID 生成UUID
func generateUUID() string {
	return fmt.Sprintf("%d", time.Now().UnixNano())
}

// EventRequest 事件请求结构
type EventRequest struct {
	UserID    string          `json:"user_id"`
	EventName string          `json:"event_name"`
	EventTime int64           `json:"event_time"`
	EventInfo json.RawMessage `json:"event_info"`
	PartDate  string          `json:"part_date"`
}
