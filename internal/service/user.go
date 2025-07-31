package service

import (
	"agent-gaming/internal/model"
	"context"
	"crypto/rand"
	"fmt"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

// UserService 用户服务
type UserService struct {
	db    *gorm.DB
	redis *redis.Client
}

// NewUserService 创建用户服务
func NewUserService(db *gorm.DB, redis *redis.Client) *UserService {
	return &UserService{
		db:    db,
		redis: redis,
	}
}

// Register 用户注册
func (s *UserService) Register(username, email, password string) (*model.User, error) {
	// 检查用户名是否已存在
	var existingUser model.User
	if err := s.db.Where("username = ? OR email = ?", username, email).First(&existingUser).Error; err == nil {
		return nil, fmt.Errorf("username or email already exists")
	}

	// 加密密码
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, fmt.Errorf("failed to hash password: %w", err)
	}

	// 创建用户
	user := &model.User{
		ID:       uuid.New().String(),
		Username: username,
		Email:    email,
		Password: string(hashedPassword),
	}

	if err := s.db.Create(user).Error; err != nil {
		return nil, fmt.Errorf("failed to create user: %w", err)
	}

	return user, nil
}

// Login 用户登录
func (s *UserService) Login(username, password string) (string, *model.User, error) {
	// 查找用户
	var user model.User
	if err := s.db.Where("username = ? OR email = ?", username, username).First(&user).Error; err != nil {
		return "", nil, fmt.Errorf("user not found")
	}

	// 验证密码
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)); err != nil {
		return "", nil, fmt.Errorf("invalid password")
	}

	// 生成JWT token
	token, err := s.generateJWT(user.ID)
	if err != nil {
		return "", nil, fmt.Errorf("failed to generate token: %w", err)
	}

	return token, &user, nil
}

// GetUserByID 根据ID获取用户
func (s *UserService) GetUserByID(userID string) (*model.User, error) {
	var user model.User
	if err := s.db.Where("id = ?", userID).First(&user).Error; err != nil {
		return nil, fmt.Errorf("user not found")
	}
	return &user, nil
}

// UpdateUser 更新用户信息
func (s *UserService) UpdateUser(userID, email string) (*model.User, error) {
	var user model.User
	if err := s.db.Where("id = ?", userID).First(&user).Error; err != nil {
		return nil, fmt.Errorf("user not found")
	}

	user.Email = email
	if err := s.db.Save(&user).Error; err != nil {
		return nil, fmt.Errorf("failed to update user: %w", err)
	}

	return &user, nil
}

// generateJWT 生成JWT token
func (s *UserService) generateJWT(userID string) (string, error) {
	// 生成随机密钥
	secret := make([]byte, 32)
	if _, err := rand.Read(secret); err != nil {
		return "", fmt.Errorf("failed to generate secret: %w", err)
	}

	// 创建JWT claims
	claims := jwt.MapClaims{
		"user_id": userID,
		"exp":     time.Now().Add(time.Hour * 24).Unix(), // 24小时过期
		"iat":     time.Now().Unix(),
	}

	// 创建token
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(secret)
	if err != nil {
		return "", fmt.Errorf("failed to sign token: %w", err)
	}

	return tokenString, nil
}

// CacheUser 缓存用户信息
func (s *UserService) CacheUser(ctx context.Context, user *model.User) error {
	key := fmt.Sprintf("user:%s", user.ID)
	data := map[string]interface{}{
		"id":       user.ID,
		"username": user.Username,
		"email":    user.Email,
	}

	return s.redis.HMSet(ctx, key, data).Err()
}

// GetCachedUser 获取缓存的用户信息
func (s *UserService) GetCachedUser(ctx context.Context, userID string) (*model.User, error) {
	key := fmt.Sprintf("user:%s", userID)
	data, err := s.redis.HGetAll(ctx, key).Result()
	if err != nil {
		return nil, err
	}

	if len(data) == 0 {
		return nil, fmt.Errorf("user not found in cache")
	}

	user := &model.User{
		ID:       data["id"],
		Username: data["username"],
		Email:    data["email"],
	}

	return user, nil
}
