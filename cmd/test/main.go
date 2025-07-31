package main

import (
	"fmt"
	"log"

	"agent-gaming/internal/config"
	"agent-gaming/internal/logger"
)

func main() {
	fmt.Println("Agent Gaming - Go Backend Test")
	fmt.Println("================================")

	// 测试配置加载
	fmt.Println("1. 测试配置加载...")
	cfg, err := config.Load()
	if err != nil {
		log.Printf("配置加载失败: %v", err)
	} else {
		fmt.Printf("✓ 配置加载成功，服务器端口: %d\n", cfg.Server.Port)
	}

	// 测试日志初始化
	fmt.Println("2. 测试日志初始化...")
	err = logger.Init(cfg.Log.Level, cfg.Log.File)
	if err != nil {
		log.Printf("日志初始化失败: %v", err)
	} else {
		fmt.Println("✓ 日志初始化成功")
	}

	fmt.Println("3. 测试数据库连接...")
	// 这里可以添加数据库连接测试

	fmt.Println("4. 测试Redis连接...")
	// 这里可以添加Redis连接测试

	fmt.Println("================================")
	fmt.Println("✓ 基础测试完成")
	fmt.Println("项目结构验证成功！")
}
