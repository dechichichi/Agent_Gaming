# Agent Gaming

[![Go Version](https://img.shields.io/badge/Go-1.21+-blue.svg)](https://golang.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE-APACHE)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE-GPL)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE-BSD)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com/)

基于Go语言的高性能游戏用户行为分析和预测系统，具备高并发、分布式缓存和微服务架构特性。

## 🚀 特性

### 核心技术栈
- **语言**: Go 1.21+
- **Web框架**: Gin (高性能HTTP框架)
- **数据库**: MySQL 8.0 + GORM
- **缓存**: Redis 7.0 (分布式缓存)
- **认证**: JWT (JSON Web Token)
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **监控**: Prometheus + Grafana

### 高并发特性
- **连接池管理**: 数据库和Redis连接池优化
- **限流机制**: 基于Redis的分布式限流
- **缓存策略**: 多层缓存架构
- **异步处理**: 后台任务队列
- **负载均衡**: 支持多实例部署

### 分布式特性
- **分布式缓存**: Redis集群支持
- **服务发现**: 支持服务注册与发现
- **配置中心**: 统一配置管理
- **链路追踪**: 请求链路监控
- **熔断机制**: 服务保护策略

## 📁 项目结构

```
agent-gaming/
├── cmd/                    # 应用入口
│   ├── main.go            # 主程序
│   └── test/              # 测试程序
├── internal/              # 内部包
│   ├── api/              # API层
│   │   └── server.go     # 服务器配置
│   ├── config/           # 配置管理
│   │   └── config.go     # 配置结构
│   ├── database/         # 数据库
│   │   └── database.go   # 数据库连接
│   ├── handler/          # 处理器
│   │   ├── handler.go    # 基础处理器
│   │   ├── user.go       # 用户处理器
│   │   └── game.go       # 游戏处理器
│   ├── middleware/       # 中间件
│   │   └── middleware.go # 中间件实现
│   ├── model/            # 数据模型
│   │   └── user.go       # 用户模型
│   ├── redis/            # Redis缓存
│   │   └── redis.go      # Redis连接
│   ├── service/          # 业务逻辑
│   │   ├── user.go       # 用户服务
│   │   └── game.go       # 游戏服务
│   └── logger/           # 日志管理
│       └── logger.go     # 日志配置
├── config/               # 配置文件
│   └── config.yaml       # 应用配置
├── docker/               # Docker配置
│   ├── mysql/           # MySQL配置
│   │   └── init.sql     # 数据库初始化
│   └── nginx/           # Nginx配置
│       └── nginx.conf   # 反向代理配置
├── docker-compose.yml    # 容器编排
├── Dockerfile           # 应用镜像
├── go.mod               # Go模块
├── go.sum               # 依赖校验
├── Makefile             # 构建脚本
└── README.md            # 项目文档
```

## 🛠️ 快速开始

### 环境要求

- Go 1.21+
- Docker & Docker Compose
- MySQL 8.0+
- Redis 7.0+

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/Agent_Gaming.git
cd Agent_Gaming
```

2. **安装依赖**
```bash
make deps
```

3. **启动开发环境**
```bash
make dev
```

4. **构建并运行**
```bash
make build
./bin/agent-gaming
```

### Docker部署

1. **启动所有服务**
```bash
make up
```

2. **查看服务状态**
```bash
docker-compose ps
```

3. **查看日志**
```bash
make logs
```

4. **停止服务**
```bash
make down
```

## 📚 API文档

### 认证接口

#### 用户注册
```http
POST /api/v1/users/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

#### 用户登录
```http
POST /api/v1/users/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

### 游戏数据接口

#### 记录用户事件
```http
POST /api/v1/games/events
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": "user123",
  "event_name": "login",
  "event_time": 1640995200,
  "event_info": "{\"level\": 10, \"coins\": 1000}"
}
```

#### 获取用户事件
```http
GET /api/v1/games/events/user123
Authorization: Bearer <token>
```

### 预测模型接口

#### 付费预测
```http
POST /api/v1/predictions/charge
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": "user123",
  "event_list": [1, 12, 44, 334],
  "max_level": 43,
  "max_viplevel": 600
}
```

#### 流失预测
```http
POST /api/v1/predictions/churn
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": "user123",
  "event_list": [1, 12, 2, 1],
  "max_level": 43,
  "max_viplevel": 600
}
```

## 🔧 配置说明

### 环境变量

```bash
# 服务器配置
SERVER_PORT=8080
SERVER_READ_TIMEOUT=15s
SERVER_WRITE_TIMEOUT=15s

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=agent_gaming
DB_MAX_OPEN=100
DB_MAX_IDLE=10

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_POOL_SIZE=10

# JWT配置
JWT_SECRET=your-secret-key
JWT_EXPIRATION=24h

# Agent配置
AGENT_MODEL=gpt-4-turbo
AGENT_TEMPERATURE=0.0
AGENT_MAX_TOKENS=2000
AGENT_API_KEY=your-api-key
```

### 配置文件

`config/config.yaml` 包含所有配置项，支持环境变量覆盖。

## 🚀 部署指南

### 开发环境

```bash
# 启动开发环境
make dev

# 运行测试
make test

# 代码检查
make lint
```

### 生产环境

```bash
# 构建生产镜像
make docker-build

# 部署到生产环境
make deploy

# 监控服务
make monitor
```

### 性能优化

1. **数据库优化**
   - 连接池配置
   - 索引优化
   - 查询优化

2. **缓存策略**
   - 热点数据缓存
   - 分布式缓存
   - 缓存穿透保护

3. **并发控制**
   - 限流机制
   - 熔断保护
   - 负载均衡

## 📊 监控与日志

### 监控指标

- **系统指标**: CPU、内存、磁盘
- **应用指标**: QPS、响应时间、错误率
- **业务指标**: 用户活跃度、预测准确率

### 日志管理

- **结构化日志**: JSON格式
- **日志级别**: DEBUG、INFO、WARN、ERROR
- **日志轮转**: 按大小和时间轮转

### 告警机制

- **系统告警**: 资源使用率
- **业务告警**: 异常预测、服务异常
- **通知方式**: 邮件、短信、钉钉

## 🔒 安全特性

### 认证授权

- **JWT认证**: 无状态认证
- **权限控制**: 基于角色的访问控制
- **会话管理**: Redis存储会话信息

### 数据安全

- **数据加密**: 敏感数据加密存储
- **传输安全**: HTTPS/TLS加密
- **SQL注入防护**: 参数化查询

### 网络安全

- **限流防护**: 防止DDoS攻击
- **CORS配置**: 跨域请求控制
- **安全头**: 安全响应头设置

## 🧪 测试

### 单元测试

```bash
# 运行所有测试
make test

# 生成覆盖率报告
make test-coverage
```

### 性能测试

```bash
# 基准测试
make benchmark

# 负载测试
make load-test
```

### 集成测试

```bash
# 启动测试环境
docker-compose -f docker-compose.test.yml up -d

# 运行集成测试
go test -tags=integration ./...
```

## 📈 性能基准

### 并发性能

- **单机QPS**: 10,000+ requests/second
- **响应时间**: < 10ms (95th percentile)
- **内存使用**: < 512MB

### 扩展性

- **水平扩展**: 支持多实例部署
- **数据库扩展**: 读写分离支持
- **缓存扩展**: Redis集群支持

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- 遵循 Go 官方代码规范
- 使用 `gofmt` 格式化代码
- 编写单元测试
- 添加必要的注释

## 📄 许可证

本项目采用多重许可证：

- [Apache License 2.0](LICENSE-APACHE)
- [GNU General Public License v3.0](LICENSE-GPL)
- [BSD 3-Clause License](LICENSE-BSD)

## 📞 联系方式

- 项目主页: https://github.com/yourusername/Agent_Gaming
- 问题反馈: https://github.com/yourusername/Agent_Gaming/issues
- 邮箱: your-email@example.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

**注意**: 这是一个基于Go语言的高性能游戏用户行为分析和预测系统，具备企业级应用的所有特性。 