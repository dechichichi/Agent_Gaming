package handler

import (
	"agent-gaming/internal/model"
	"agent-gaming/internal/service"
	"context"
	"encoding/json"
	"fmt"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

// GameHandler 游戏处理器
type GameHandler struct {
	*BaseHandler
	gameService *service.GameService
}

// NewGameHandler 创建游戏处理器
func NewGameHandler(db *gorm.DB, redis *redis.Client) *GameHandler {
	return &GameHandler{
		BaseHandler: NewBaseHandler(db, redis),
		gameService: service.NewGameService(db, redis),
	}
}

// EventRequest 事件请求
type EventRequest struct {
	UserID    string          `json:"user_id" binding:"required"`
	EventName string          `json:"event_name" binding:"required"`
	EventTime int64           `json:"event_time" binding:"required"`
	EventInfo json.RawMessage `json:"event_info"`
	PartDate  string          `json:"part_date"`
}

// AnalyticsRequest 分析请求
type AnalyticsRequest struct {
	UserID    string `json:"user_id" binding:"required"`
	StartDate string `json:"start_date"`
	EndDate   string `json:"end_date"`
	Limit     int    `json:"limit"`
}

// RecordEvent 记录用户事件
func (h *GameHandler) RecordEvent(c *gin.Context) {
	var req EventRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		BadRequest(c, "Invalid request data")
		return
	}

	// 使用缓存减少数据库压力
	cacheKey := fmt.Sprintf("user_event:%s:%d", req.UserID, req.EventTime)
	ctx := context.Background()

	// 检查缓存
	if _, err := h.redis.Get(ctx, cacheKey).Result(); err == nil {
		Success(c, gin.H{"message": "Event already recorded", "cached": true})
		return
	}

	// 创建事件记录
	event := &model.UserEvent{
		ID:        uuid.New().String(),
		UserID:    req.UserID,
		EventName: req.EventName,
		EventTime: req.EventTime,
		EventInfo: string(req.EventInfo),
		PartDate:  req.PartDate,
	}

	// 异步处理事件
	go func() {
		if err := h.gameService.RecordEventAsync(event); err != nil {
			// 记录错误日志
			fmt.Printf("Failed to record event: %v\n", err)
		}
	}()

	// 缓存事件记录（5分钟）
	h.redis.Set(ctx, cacheKey, "recorded", 5*time.Minute)

	Success(c, gin.H{
		"message":  "Event recorded successfully",
		"event_id": event.ID,
	})
}

// GetUserEvents 获取用户事件
func (h *GameHandler) GetUserEvents(c *gin.Context) {
	userID := c.Param("user_id")
	if userID == "" {
		BadRequest(c, "User ID is required")
		return
	}

	// 解析查询参数
	limitStr := c.DefaultQuery("limit", "100")
	limit, err := strconv.Atoi(limitStr)
	if err != nil {
		limit = 100
	}

	// 使用缓存获取用户事件
	cacheKey := fmt.Sprintf("user_events:%s:%d", userID, limit)
	ctx := context.Background()

	// 尝试从缓存获取
	if cached, err := h.redis.Get(ctx, cacheKey).Result(); err == nil {
		var events []model.UserEvent
		if err := json.Unmarshal([]byte(cached), &events); err == nil {
			Success(c, gin.H{
				"events": events,
				"cached": true,
			})
			return
		}
	}

	// 从数据库获取
	events, err := h.gameService.GetUserEvents(userID, limit)
	if err != nil {
		InternalServerError(c, "Failed to get user events")
		return
	}

	// 缓存结果（10分钟）
	if data, err := json.Marshal(events); err == nil {
		h.redis.Set(ctx, cacheKey, string(data), 10*time.Minute)
	}

	Success(c, gin.H{
		"events": events,
		"cached": false,
	})
}

// GetAnalytics 获取分析数据
func (h *GameHandler) GetAnalytics(c *gin.Context) {
	var req AnalyticsRequest
	if err := c.ShouldBindQuery(&req); err != nil {
		BadRequest(c, "Invalid query parameters")
		return
	}

	// 使用缓存获取分析数据
	cacheKey := fmt.Sprintf("analytics:%s:%s:%s", req.UserID, req.StartDate, req.EndDate)
	ctx := context.Background()

	// 尝试从缓存获取
	if cached, err := h.redis.Get(ctx, cacheKey).Result(); err == nil {
		var analytics map[string]interface{}
		if err := json.Unmarshal([]byte(cached), &analytics); err == nil {
			Success(c, gin.H{
				"analytics": analytics,
				"cached":    true,
			})
			return
		}
	}

	// 计算分析数据
	analytics, err := h.gameService.GetUserAnalytics(req.UserID, req.StartDate, req.EndDate)
	if err != nil {
		InternalServerError(c, "Failed to get analytics")
		return
	}

	// 缓存结果（30分钟）
	if data, err := json.Marshal(analytics); err == nil {
		h.redis.Set(ctx, cacheKey, string(data), 30*time.Minute)
	}

	Success(c, gin.H{
		"analytics": analytics,
		"cached":    false,
	})
}

// GetUserStats 获取用户统计
func (h *GameHandler) GetUserStats(c *gin.Context) {
	userID := c.Param("user_id")
	if userID == "" {
		BadRequest(c, "User ID is required")
		return
	}

	// 使用缓存获取用户统计
	cacheKey := fmt.Sprintf("user_stats:%s", userID)
	ctx := context.Background()

	// 尝试从缓存获取
	if cached, err := h.redis.Get(ctx, cacheKey).Result(); err == nil {
		var stats map[string]interface{}
		if err := json.Unmarshal([]byte(cached), &stats); err == nil {
			Success(c, gin.H{
				"stats":  stats,
				"cached": true,
			})
			return
		}
	}

	// 计算用户统计
	stats, err := h.gameService.GetUserStats(userID)
	if err != nil {
		InternalServerError(c, "Failed to get user stats")
		return
	}

	// 缓存结果（15分钟）
	if data, err := json.Marshal(stats); err == nil {
		h.redis.Set(ctx, cacheKey, string(data), 15*time.Minute)
	}

	Success(c, gin.H{
		"stats":  stats,
		"cached": false,
	})
}

// convertToServiceEvents 转换事件类型
func convertToServiceEvents(events []EventRequest) []service.EventRequest {
	serviceEvents := make([]service.EventRequest, len(events))
	for i, event := range events {
		serviceEvents[i] = service.EventRequest{
			UserID:    event.UserID,
			EventName: event.EventName,
			EventTime: event.EventTime,
			EventInfo: event.EventInfo,
			PartDate:  event.PartDate,
		}
	}
	return serviceEvents
}

// BatchRecordEvents 批量记录事件
func (h *GameHandler) BatchRecordEvents(c *gin.Context) {
	var events []EventRequest
	if err := c.ShouldBindJSON(&events); err != nil {
		BadRequest(c, "Invalid request data")
		return
	}

	if len(events) > 1000 {
		BadRequest(c, "Too many events in batch (max 1000)")
		return
	}

	// 异步批量处理
	go func() {
		if err := h.gameService.BatchRecordEvents(convertToServiceEvents(events)); err != nil {
			fmt.Printf("Failed to batch record events: %v\n", err)
		}
	}()

	Success(c, gin.H{
		"message": fmt.Sprintf("Batch processing %d events", len(events)),
		"count":   len(events),
	})
}
