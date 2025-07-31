package handler

import (
	"agent-gaming/internal/service"

	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis/v8"
	"gorm.io/gorm"
)

// UserHandler 用户处理器
type UserHandler struct {
	*BaseHandler
	userService *service.UserService
}

// NewUserHandler 创建用户处理器
func NewUserHandler(db *gorm.DB, redis *redis.Client) *UserHandler {
	return &UserHandler{
		BaseHandler: NewBaseHandler(db, redis),
		userService: service.NewUserService(db, redis),
	}
}

// RegisterRequest 注册请求
type RegisterRequest struct {
	Username string `json:"username" binding:"required"`
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required,min=6"`
}

// LoginRequest 登录请求
type LoginRequest struct {
	Username string `json:"username" binding:"required"`
	Password string `json:"password" binding:"required"`
}

// Register 用户注册
func (h *UserHandler) Register(c *gin.Context) {
	var req RegisterRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		BadRequest(c, "Invalid request data")
		return
	}

	user, err := h.userService.Register(req.Username, req.Email, req.Password)
	if err != nil {
		InternalServerError(c, err.Error())
		return
	}

	Success(c, gin.H{
		"user": gin.H{
			"id":       user.ID,
			"username": user.Username,
			"email":    user.Email,
		},
	})
}

// Login 用户登录
func (h *UserHandler) Login(c *gin.Context) {
	var req LoginRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		BadRequest(c, "Invalid request data")
		return
	}

	token, user, err := h.userService.Login(req.Username, req.Password)
	if err != nil {
		Unauthorized(c, "Invalid credentials")
		return
	}

	Success(c, gin.H{
		"token": token,
		"user": gin.H{
			"id":       user.ID,
			"username": user.Username,
			"email":    user.Email,
		},
	})
}

// GetProfile 获取用户信息
func (h *UserHandler) GetProfile(c *gin.Context) {
	userID := c.GetString("user_id")
	if userID == "" {
		Unauthorized(c, "User not authenticated")
		return
	}

	user, err := h.userService.GetUserByID(userID)
	if err != nil {
		NotFound(c, "User not found")
		return
	}

	Success(c, gin.H{
		"user": gin.H{
			"id":         user.ID,
			"username":   user.Username,
			"email":      user.Email,
			"created_at": user.CreatedAt,
		},
	})
}

// UpdateProfile 更新用户信息
func (h *UserHandler) UpdateProfile(c *gin.Context) {
	userID := c.GetString("user_id")
	if userID == "" {
		Unauthorized(c, "User not authenticated")
		return
	}

	var req struct {
		Email string `json:"email" binding:"email"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		BadRequest(c, "Invalid request data")
		return
	}

	user, err := h.userService.UpdateUser(userID, req.Email)
	if err != nil {
		InternalServerError(c, err.Error())
		return
	}

	Success(c, gin.H{
		"user": gin.H{
			"id":         user.ID,
			"username":   user.Username,
			"email":      user.Email,
			"updated_at": user.UpdatedAt,
		},
	})
}
