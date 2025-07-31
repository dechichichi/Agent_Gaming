package redis

import (
	"agent-gaming/internal/config"
	"context"
	"fmt"
	"time"

	"github.com/go-redis/redis/v8"
)

// Client Redis客户端
var Client *redis.Client

// Init 初始化Redis连接
func Init(cfg config.RedisConfig) (*redis.Client, error) {
	client := redis.NewClient(&redis.Options{
		Addr:     cfg.GetRedisAddr(),
		Password: cfg.Password,
		DB:       cfg.DB,
		PoolSize: cfg.PoolSize,
	})

	// 测试连接
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := client.Ping(ctx).Err(); err != nil {
		return nil, fmt.Errorf("failed to ping Redis: %w", err)
	}

	Client = client
	return client, nil
}

// GetClient 获取Redis客户端
func GetClient() *redis.Client {
	return Client
}

// Close 关闭Redis连接
func Close() error {
	if Client != nil {
		return Client.Close()
	}
	return nil
}

// Set 设置键值对
func Set(ctx context.Context, key string, value interface{}, expiration time.Duration) error {
	return Client.Set(ctx, key, value, expiration).Err()
}

// Get 获取值
func Get(ctx context.Context, key string) (string, error) {
	return Client.Get(ctx, key).Result()
}

// Del 删除键
func Del(ctx context.Context, keys ...string) error {
	return Client.Del(ctx, keys...).Err()
}

// Exists 检查键是否存在
func Exists(ctx context.Context, keys ...string) (int64, error) {
	return Client.Exists(ctx, keys...).Result()
}

// Incr 递增
func Incr(ctx context.Context, key string) (int64, error) {
	return Client.Incr(ctx, key).Result()
}

// IncrBy 按指定值递增
func IncrBy(ctx context.Context, key string, value int64) (int64, error) {
	return Client.IncrBy(ctx, key, value).Result()
}

// HSet 设置哈希表字段
func HSet(ctx context.Context, key string, values ...interface{}) error {
	return Client.HSet(ctx, key, values...).Err()
}

// HGet 获取哈希表字段
func HGet(ctx context.Context, key, field string) (string, error) {
	return Client.HGet(ctx, key, field).Result()
}

// HGetAll 获取哈希表所有字段
func HGetAll(ctx context.Context, key string) (map[string]string, error) {
	return Client.HGetAll(ctx, key).Result()
}

// HDel 删除哈希表字段
func HDel(ctx context.Context, key string, fields ...string) error {
	return Client.HDel(ctx, key, fields...).Err()
}
