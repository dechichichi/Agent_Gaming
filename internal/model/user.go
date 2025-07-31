package model

import (
	"time"

	"gorm.io/gorm"
)

// User 用户模型
type User struct {
	ID        string         `json:"id" gorm:"primaryKey;type:varchar(36)"`
	Username  string         `json:"username" gorm:"uniqueIndex;not null;type:varchar(50)"`
	Email     string         `json:"email" gorm:"uniqueIndex;not null;type:varchar(100)"`
	Password  string         `json:"-" gorm:"not null;type:varchar(255)"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`
}

// TableName 指定表名
func (User) TableName() string {
	return "users"
}

// UserEvent 用户事件模型
type UserEvent struct {
	ID        string         `json:"id" gorm:"primaryKey;type:varchar(36)"`
	UserID    string         `json:"user_id" gorm:"index;not null;type:varchar(36)"`
	EventName string         `json:"event_name" gorm:"not null;type:varchar(100)"`
	EventTime int64          `json:"event_time" gorm:"not null"`
	EventInfo string         `json:"event_info" gorm:"type:text"`
	PartDate  string         `json:"part_date" gorm:"type:varchar(20)"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`
}

// TableName 指定表名
func (UserEvent) TableName() string {
	return "user_event_log"
}

// UserLabel 用户标签模型
type UserLabel struct {
	ID        string         `json:"id" gorm:"primaryKey;type:varchar(36)"`
	UserID    string         `json:"user_id" gorm:"index;not null;type:varchar(36)"`
	LabelType string         `json:"label_type" gorm:"not null;type:varchar(20)"` // charge, lose
	Target    int            `json:"target" gorm:"not null"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`
}

// TableName 指定表名
func (UserLabel) TableName() string {
	return "user_label"
}

// SequentialOutput 序列输出模型
type SequentialOutput struct {
	ID             string         `json:"id" gorm:"primaryKey;type:varchar(36)"`
	UserID         string         `json:"user_id" gorm:"index;not null;type:varchar(36)"`
	TrainStartDate string         `json:"train_start_date" gorm:"type:varchar(20)"`
	TrainEndDate   string         `json:"train_end_date" gorm:"type:varchar(20)"`
	TestStartDate  string         `json:"test_start_date" gorm:"type:varchar(20)"`
	TestEndDate    string         `json:"test_end_date" gorm:"type:varchar(20)"`
	IsPrepay       int            `json:"is_prepay" gorm:"not null"`
	Target         int            `json:"target" gorm:"not null"`
	PartDate       string         `json:"part_date" gorm:"type:varchar(20)"`
	EventList      string         `json:"event_list" gorm:"type:text"`
	StatsItemList  string         `json:"stats_item_list" gorm:"type:text"`
	StatsEventList string         `json:"stats_event_list" gorm:"type:text"`
	NumEvent       int            `json:"num_event" gorm:"not null"`
	MaxLevel       int            `json:"max_level" gorm:"not null"`
	MaxVipLevel    int            `json:"max_viplevel" gorm:"not null"`
	ValRow         int            `json:"val_row" gorm:"not null"`
	CreatedAt      time.Time      `json:"created_at"`
	UpdatedAt      time.Time      `json:"updated_at"`
	DeletedAt      gorm.DeletedAt `json:"-" gorm:"index"`
}

// TableName 指定表名
func (SequentialOutput) TableName() string {
	return "sequential_output"
}

// PredictionModel 预测模型
type PredictionModel struct {
	ID        string         `json:"id" gorm:"primaryKey;type:varchar(36)"`
	Name      string         `json:"name" gorm:"uniqueIndex;not null;type:varchar(100)"`
	Type      string         `json:"type" gorm:"not null;type:varchar(20)"`   // charge, lose
	Status    string         `json:"status" gorm:"not null;type:varchar(20)"` // training, trained, failed
	Version   string         `json:"version" gorm:"type:varchar(20)"`
	Accuracy  float64        `json:"accuracy" gorm:"type:decimal(5,4)"`
	F1Score   float64        `json:"f1_score" gorm:"type:decimal(5,4)"`
	ModelPath string         `json:"model_path" gorm:"type:varchar(255)"`
	Config    string         `json:"config" gorm:"type:text"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`
}

// TableName 指定表名
func (PredictionModel) TableName() string {
	return "prediction_models"
}
