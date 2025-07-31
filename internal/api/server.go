package api

import (
	"agent-gaming/internal/config"
	"agent-gaming/internal/handler"
	"agent-gaming/internal/middleware"

	"github.com/gin-gonic/gin"
	redisClient "github.com/go-redis/redis/v8"
	"gorm.io/gorm"
)

// Server API服务器
type Server struct {
	config *config.Config
	db     *gorm.DB
	redis  *redisClient.Client
	router *gin.Engine
}

// NewServer 创建新的API服务器
func NewServer(cfg *config.Config, db *gorm.DB, redisClient *redisClient.Client) *Server {
	server := &Server{
		config: cfg,
		db:     db,
		redis:  redisClient,
		router: gin.New(),
	}

	server.setupMiddleware()
	server.setupRoutes()

	return server
}

// setupMiddleware 设置中间件
func (s *Server) setupMiddleware() {
	// 使用gin的默认中间件
	s.router.Use(gin.Logger())
	s.router.Use(gin.Recovery())

	// 自定义中间件
	s.router.Use(middleware.CORS())
	s.router.Use(middleware.RequestID())
	s.router.Use(middleware.Logger())
	s.router.Use(middleware.RateLimit(s.redis))
}

// setupRoutes 设置路由
func (s *Server) setupRoutes() {
	// 健康检查
	s.router.GET("/health", handler.HealthCheck)

	// API版本组
	v1 := s.router.Group("/api/v1")
	{
		// 用户相关路由
		userHandler := handler.NewUserHandler(s.db, s.redis)
		users := v1.Group("/users")
		{
			users.POST("/register", userHandler.Register)
			users.POST("/login", userHandler.Login)
			users.GET("/profile", middleware.Auth(s.config.JWT.Secret), userHandler.GetProfile)
			users.PUT("/profile", middleware.Auth(s.config.JWT.Secret), userHandler.UpdateProfile)
		}

		// 游戏数据相关路由
		gameHandler := handler.NewGameHandler(s.db, s.redis)
		games := v1.Group("/games")
		{
			games.POST("/events", middleware.Auth(s.config.JWT.Secret), gameHandler.RecordEvent)
			games.GET("/events/:user_id", middleware.Auth(s.config.JWT.Secret), gameHandler.GetUserEvents)
			games.GET("/analytics", middleware.Auth(s.config.JWT.Secret), gameHandler.GetAnalytics)
		}

		// 预测模型相关路由 - TODO: 实现处理器
		// predictions := v1.Group("/predictions")
		// {
		// 	predictions.POST("/charge", middleware.Auth(s.config.JWT.Secret), predictionHandler.PredictCharge)
		// 	predictions.POST("/churn", middleware.Auth(s.config.JWT.Secret), predictionHandler.PredictChurn)
		// 	predictions.GET("/models", middleware.Auth(s.config.JWT.Secret), predictionHandler.GetModels)
		// 	predictions.POST("/models/train", middleware.Auth(s.config.JWT.Secret), predictionHandler.TrainModel)
		// }

		// Agent相关路由 - TODO: 实现处理器
		// agents := v1.Group("/agents")
		// {
		// 	agents.POST("/analyze", middleware.Auth(s.config.JWT.Secret), agentHandler.AnalyzeUser)
		// 	agents.POST("/intervention", middleware.Auth(s.config.JWT.Secret), agentHandler.GenerateIntervention)
		// 	agents.GET("/recommendations/:user_id", middleware.Auth(s.config.JWT.Secret), agentHandler.GetRecommendations)
		// }

		// 数据管理相关路由 - TODO: 实现处理器
		// data := v1.Group("/data")
		// {
		// 	data.POST("/import", middleware.Auth(s.config.JWT.Secret), dataHandler.ImportData)
		// 	data.GET("/export", middleware.Auth(s.config.JWT.Secret), dataHandler.ExportData)
		// 	data.GET("/statistics", middleware.Auth(s.config.JWT.Secret), dataHandler.GetStatistics)
		// }
	}

	// WebSocket路由 - TODO: 实现处理器
	// wsHandler := handler.NewWebSocketHandler(s.redis)
	// s.router.GET("/ws", wsHandler.HandleWebSocket)
}

// Router 获取路由
func (s *Server) Router() *gin.Engine {
	return s.router
}
