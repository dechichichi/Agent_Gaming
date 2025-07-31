package middleware

import (
	"context"
	"fmt"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis/v8"
	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
	"github.com/sirupsen/logrus"
)

// CORS 跨域中间件
func CORS() gin.HandlerFunc {
	return gin.HandlerFunc(func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", "*")
		c.Header("Access-Control-Allow-Credentials", "true")
		c.Header("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Header("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	})
}

// RequestID 请求ID中间件
func RequestID() gin.HandlerFunc {
	return gin.HandlerFunc(func(c *gin.Context) {
		requestID := c.GetHeader("X-Request-ID")
		if requestID == "" {
			requestID = uuid.New().String()
		}
		c.Header("X-Request-ID", requestID)
		c.Set("request_id", requestID)
		c.Next()
	})
}

// Logger 日志中间件
func Logger() gin.HandlerFunc {
	return gin.HandlerFunc(func(c *gin.Context) {
		start := time.Now()
		path := c.Request.URL.Path
		raw := c.Request.URL.RawQuery

		c.Next()

		latency := time.Since(start)
		clientIP := c.ClientIP()
		method := c.Request.Method
		statusCode := c.Writer.Status()
		bodySize := c.Writer.Size()

		if raw != "" {
			path = path + "?" + raw
		}

		logrus.WithFields(logrus.Fields{
			"status_code": statusCode,
			"latency":     latency,
			"client_ip":   clientIP,
			"method":      method,
			"path":        path,
			"body_size":   bodySize,
		}).Info("HTTP Request")
	})
}

// RateLimit 限流中间件
func RateLimit(redisClient *redis.Client) gin.HandlerFunc {
	return gin.HandlerFunc(func(c *gin.Context) {
		clientIP := c.ClientIP()
		key := fmt.Sprintf("rate_limit:%s", clientIP)

		ctx := context.Background()
		count, err := redisClient.Incr(ctx, key).Result()
		if err != nil {
			logrus.Errorf("Rate limit error: %v", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Rate limit error"})
			c.Abort()
			return
		}

		// 设置过期时间（1分钟）
		if count == 1 {
			redisClient.Expire(ctx, key, time.Minute)
		}

		// 限制每分钟100次请求
		if count > 100 {
			c.JSON(http.StatusTooManyRequests, gin.H{"error": "Rate limit exceeded"})
			c.Abort()
			return
		}

		c.Header("X-RateLimit-Limit", "100")
		c.Header("X-RateLimit-Remaining", strconv.FormatInt(100-count, 10))
		c.Next()
	})
}

// Auth JWT认证中间件
func Auth(secret string) gin.HandlerFunc {
	return gin.HandlerFunc(func(c *gin.Context) {
		tokenString := c.GetHeader("Authorization")
		if tokenString == "" {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header required"})
			c.Abort()
			return
		}

		// 移除Bearer前缀
		if len(tokenString) > 7 && tokenString[:7] == "Bearer " {
			tokenString = tokenString[7:]
		}

		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
			}
			return []byte(secret), nil
		})

		if err != nil {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
			c.Abort()
			return
		}

		if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
			userID, ok := claims["user_id"].(string)
			if !ok {
				c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token claims"})
				c.Abort()
				return
			}
			c.Set("user_id", userID)
			c.Next()
		} else {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
			c.Abort()
			return
		}
	})
}

// Cache 缓存中间件
func Cache(redisClient *redis.Client, expiration time.Duration) gin.HandlerFunc {
	return gin.HandlerFunc(func(c *gin.Context) {
		key := fmt.Sprintf("cache:%s", c.Request.URL.String())
		ctx := context.Background()

		// 尝试从缓存获取
		cached, err := redisClient.Get(ctx, key).Result()
		if err == nil {
			c.Header("X-Cache", "HIT")
			c.Data(http.StatusOK, "application/json", []byte(cached))
			c.Abort()
			return
		}

		c.Header("X-Cache", "MISS")
		c.Next()
	})
}
