package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"agent-gaming/internal/api"
	"agent-gaming/internal/config"
	"agent-gaming/internal/database"
	"agent-gaming/internal/logger"
	"agent-gaming/internal/redis"

	"github.com/sirupsen/logrus"
)

func main() {
	// 加载配置
	cfg, err := config.Load()
	if err != nil {
		logrus.Fatalf("Failed to load config: %v", err)
	}

	// 初始化日志
	logger.Init(cfg.Log.Level, cfg.Log.File)

	// 初始化数据库连接
	db, err := database.Init(cfg.Database)
	if err != nil {
		logrus.Fatalf("Failed to initialize database: %v", err)
	}

	// 初始化Redis连接
	redisClient, err := redis.Init(cfg.Redis)
	if err != nil {
		logrus.Fatalf("Failed to initialize Redis: %v", err)
	}

	// 初始化API服务
	apiServer := api.NewServer(cfg, db, redisClient)

	// 创建HTTP服务器
	srv := &http.Server{
		Addr:         fmt.Sprintf(":%d", cfg.Server.Port),
		Handler:      apiServer.Router(),
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// 启动服务器
	go func() {
		logrus.Infof("Starting server on port %d", cfg.Server.Port)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logrus.Fatalf("Failed to start server: %v", err)
		}
	}()

	// 等待中断信号
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	logrus.Info("Shutting down server...")

	// 优雅关闭
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		logrus.Fatalf("Server forced to shutdown: %v", err)
	}

	logrus.Info("Server exited")
}
