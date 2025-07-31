package config

import (
	"fmt"
	"time"

	"github.com/joho/godotenv"
	"github.com/spf13/viper"
)

// Config 应用配置结构
type Config struct {
	Server   ServerConfig   `mapstructure:"server"`
	Database DatabaseConfig `mapstructure:"database"`
	Redis    RedisConfig    `mapstructure:"redis"`
	Log      LogConfig      `mapstructure:"log"`
	JWT      JWTConfig      `mapstructure:"jwt"`
	Agent    AgentConfig    `mapstructure:"agent"`
}

// ServerConfig 服务器配置
type ServerConfig struct {
	Port         int           `mapstructure:"port"`
	ReadTimeout  time.Duration `mapstructure:"read_timeout"`
	WriteTimeout time.Duration `mapstructure:"write_timeout"`
	IdleTimeout  time.Duration `mapstructure:"idle_timeout"`
}

// DatabaseConfig 数据库配置
type DatabaseConfig struct {
	Host     string `mapstructure:"host"`
	Port     int    `mapstructure:"port"`
	User     string `mapstructure:"user"`
	Password string `mapstructure:"password"`
	DBName   string `mapstructure:"dbname"`
	Charset  string `mapstructure:"charset"`
	MaxOpen  int    `mapstructure:"max_open"`
	MaxIdle  int    `mapstructure:"max_idle"`
}

// RedisConfig Redis配置
type RedisConfig struct {
	Host     string `mapstructure:"host"`
	Port     int    `mapstructure:"port"`
	Password string `mapstructure:"password"`
	DB       int    `mapstructure:"db"`
	PoolSize int    `mapstructure:"pool_size"`
}

// LogConfig 日志配置
type LogConfig struct {
	Level string `mapstructure:"level"`
	File  string `mapstructure:"file"`
}

// JWTConfig JWT配置
type JWTConfig struct {
	Secret     string        `mapstructure:"secret"`
	Expiration time.Duration `mapstructure:"expiration"`
}

// AgentConfig Agent配置
type AgentConfig struct {
	Model       string  `mapstructure:"model"`
	Temperature float64 `mapstructure:"temperature"`
	MaxTokens   int     `mapstructure:"max_tokens"`
	APIKey      string  `mapstructure:"api_key"`
}

// Load 加载配置
func Load() (*Config, error) {
	// 加载环境变量文件
	if err := godotenv.Load(); err != nil {
		// 如果.env文件不存在，继续执行
	}

	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("./config")
	viper.AddConfigPath("../config")
	viper.AddConfigPath("../../config")

	// 设置默认值
	setDefaults()

	// 绑定环境变量
	bindEnvs()

	// 读取配置文件
	if err := viper.ReadInConfig(); err != nil {
		// 如果配置文件不存在，使用默认值
	}

	var config Config
	if err := viper.Unmarshal(&config); err != nil {
		return nil, fmt.Errorf("failed to unmarshal config: %w", err)
	}

	return &config, nil
}

// setDefaults 设置默认配置
func setDefaults() {
	// 服务器默认配置
	viper.SetDefault("server.port", 8080)
	viper.SetDefault("server.read_timeout", "15s")
	viper.SetDefault("server.write_timeout", "15s")
	viper.SetDefault("server.idle_timeout", "60s")

	// 数据库默认配置
	viper.SetDefault("database.host", "localhost")
	viper.SetDefault("database.port", 3306)
	viper.SetDefault("database.user", "root")
	viper.SetDefault("database.password", "")
	viper.SetDefault("database.dbname", "agent_gaming")
	viper.SetDefault("database.charset", "utf8mb4")
	viper.SetDefault("database.max_open", 100)
	viper.SetDefault("database.max_idle", 10)

	// Redis默认配置
	viper.SetDefault("redis.host", "localhost")
	viper.SetDefault("redis.port", 6379)
	viper.SetDefault("redis.password", "")
	viper.SetDefault("redis.db", 0)
	viper.SetDefault("redis.pool_size", 10)

	// 日志默认配置
	viper.SetDefault("log.level", "info")
	viper.SetDefault("log.file", "logs/app.log")

	// JWT默认配置
	viper.SetDefault("jwt.secret", "your-secret-key")
	viper.SetDefault("jwt.expiration", "24h")

	// Agent默认配置
	viper.SetDefault("agent.model", "gpt-4-turbo")
	viper.SetDefault("agent.temperature", 0.0)
	viper.SetDefault("agent.max_tokens", 2000)
}

// bindEnvs 绑定环境变量
func bindEnvs() {
	// 服务器环境变量
	viper.BindEnv("server.port", "SERVER_PORT")
	viper.BindEnv("server.read_timeout", "SERVER_READ_TIMEOUT")
	viper.BindEnv("server.write_timeout", "SERVER_WRITE_TIMEOUT")
	viper.BindEnv("server.idle_timeout", "SERVER_IDLE_TIMEOUT")

	// 数据库环境变量
	viper.BindEnv("database.host", "DB_HOST")
	viper.BindEnv("database.port", "DB_PORT")
	viper.BindEnv("database.user", "DB_USER")
	viper.BindEnv("database.password", "DB_PASSWORD")
	viper.BindEnv("database.dbname", "DB_NAME")
	viper.BindEnv("database.charset", "DB_CHARSET")
	viper.BindEnv("database.max_open", "DB_MAX_OPEN")
	viper.BindEnv("database.max_idle", "DB_MAX_IDLE")

	// Redis环境变量
	viper.BindEnv("redis.host", "REDIS_HOST")
	viper.BindEnv("redis.port", "REDIS_PORT")
	viper.BindEnv("redis.password", "REDIS_PASSWORD")
	viper.BindEnv("redis.db", "REDIS_DB")
	viper.BindEnv("redis.pool_size", "REDIS_POOL_SIZE")

	// 日志环境变量
	viper.BindEnv("log.level", "LOG_LEVEL")
	viper.BindEnv("log.file", "LOG_FILE")

	// JWT环境变量
	viper.BindEnv("jwt.secret", "JWT_SECRET")
	viper.BindEnv("jwt.expiration", "JWT_EXPIRATION")

	// Agent环境变量
	viper.BindEnv("agent.model", "AGENT_MODEL")
	viper.BindEnv("agent.temperature", "AGENT_TEMPERATURE")
	viper.BindEnv("agent.max_tokens", "AGENT_MAX_TOKENS")
	viper.BindEnv("agent.api_key", "AGENT_API_KEY")
}

// GetDSN 获取数据库连接字符串
func (c *DatabaseConfig) GetDSN() string {
	return fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=%s&parseTime=True&loc=Local",
		c.User, c.Password, c.Host, c.Port, c.DBName, c.Charset)
}

// GetRedisAddr 获取Redis地址
func (c *RedisConfig) GetRedisAddr() string {
	return fmt.Sprintf("%s:%d", c.Host, c.Port)
}
