# 变量定义
APP_NAME=agent-gaming
VERSION=1.0.0
DOCKER_IMAGE=agent-gaming:$(VERSION)

# 默认目标
.PHONY: help
help: ## 显示帮助信息
	@echo "Agent Gaming - Go Backend"
	@echo "========================"
	@echo "可用命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 开发相关
.PHONY: dev
dev: ## 启动开发环境
	@echo "启动开发环境..."
	docker-compose up -d mysql redis
	@echo "等待数据库启动..."
	@sleep 10
	go run cmd/main.go

.PHONY: build
build: ## 构建应用
	@echo "构建应用..."
	CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o bin/$(APP_NAME) ./cmd/main.go

.PHONY: test
test: ## 运行测试
	@echo "运行测试..."
	go test -v ./...

.PHONY: test-coverage
test-coverage: ## 运行测试并生成覆盖率报告
	@echo "运行测试并生成覆盖率报告..."
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html
	@echo "覆盖率报告已生成: coverage.html"

# Docker相关
.PHONY: docker-build
docker-build: ## 构建Docker镜像
	@echo "构建Docker镜像..."
	docker build -t $(DOCKER_IMAGE) .

.PHONY: docker-run
docker-run: ## 运行Docker容器
	@echo "运行Docker容器..."
	docker run -p 8080:8080 --name $(APP_NAME) $(DOCKER_IMAGE)

.PHONY: docker-stop
docker-stop: ## 停止Docker容器
	@echo "停止Docker容器..."
	docker stop $(APP_NAME) || true
	docker rm $(APP_NAME) || true

# Docker Compose相关
.PHONY: up
up: ## 启动所有服务
	@echo "启动所有服务..."
	docker-compose up -d

.PHONY: down
down: ## 停止所有服务
	@echo "停止所有服务..."
	docker-compose down

.PHONY: logs
logs: ## 查看服务日志
	@echo "查看服务日志..."
	docker-compose logs -f

.PHONY: restart
restart: ## 重启所有服务
	@echo "重启所有服务..."
	docker-compose restart

# 数据库相关
.PHONY: db-migrate
db-migrate: ## 运行数据库迁移
	@echo "运行数据库迁移..."
	go run cmd/migrate/main.go

.PHONY: db-seed
db-seed: ## 填充测试数据
	@echo "填充测试数据..."
	go run cmd/seed/main.go

# 代码质量
.PHONY: lint
lint: ## 运行代码检查
	@echo "运行代码检查..."
	golangci-lint run

.PHONY: fmt
fmt: ## 格式化代码
	@echo "格式化代码..."
	go fmt ./...

.PHONY: vet
vet: ## 运行go vet
	@echo "运行go vet..."
	go vet ./...

# 依赖管理
.PHONY: deps
deps: ## 下载依赖
	@echo "下载依赖..."
	go mod download

.PHONY: deps-update
deps-update: ## 更新依赖
	@echo "更新依赖..."
	go get -u ./...
	go mod tidy

# 清理
.PHONY: clean
clean: ## 清理构建文件
	@echo "清理构建文件..."
	rm -rf bin/
	rm -rf coverage.out coverage.html
	go clean

.PHONY: docker-clean
docker-clean: ## 清理Docker资源
	@echo "清理Docker资源..."
	docker system prune -f
	docker volume prune -f

# 部署相关
.PHONY: deploy
deploy: ## 部署到生产环境
	@echo "部署到生产环境..."
	docker-compose -f docker-compose.prod.yml up -d

.PHONY: deploy-stop
deploy-stop: ## 停止生产环境
	@echo "停止生产环境..."
	docker-compose -f docker-compose.prod.yml down

# 监控相关
.PHONY: monitor
monitor: ## 启动监控
	@echo "启动监控..."
	docker-compose -f docker-compose.monitoring.yml up -d

.PHONY: monitor-stop
monitor-stop: ## 停止监控
	@echo "停止监控..."
	docker-compose -f docker-compose.monitoring.yml down

# 备份相关
.PHONY: backup
backup: ## 备份数据库
	@echo "备份数据库..."
	docker exec agent_gaming_mysql mysqldump -u root -prootpassword agent_gaming > backup/$(shell date +%Y%m%d_%H%M%S)_backup.sql

.PHONY: restore
restore: ## 恢复数据库
	@echo "恢复数据库..."
	@read -p "请输入备份文件路径: " file; \
	docker exec -i agent_gaming_mysql mysql -u root -prootpassword agent_gaming < $$file

# 性能测试
.PHONY: benchmark
benchmark: ## 运行性能测试
	@echo "运行性能测试..."
	go test -bench=. -benchmem ./...

.PHONY: load-test
load-test: ## 运行负载测试
	@echo "运行负载测试..."
	@if command -v wrk >/dev/null 2>&1; then \
		wrk -t12 -c400 -d30s http://localhost:8080/health; \
	else \
		echo "请安装wrk: https://github.com/wg/wrk"; \
	fi

# 安全扫描
.PHONY: security-scan
security-scan: ## 运行安全扫描
	@echo "运行安全扫描..."
	@if command -v gosec >/dev/null 2>&1; then \
		gosec ./...; \
	else \
		echo "请安装gosec: go install github.com/securecodewarrior/gosec/v2/cmd/gosec@latest"; \
	fi

# 文档生成
.PHONY: docs
docs: ## 生成API文档
	@echo "生成API文档..."
	@if command -v swag >/dev/null 2>&1; then \
		swag init -g cmd/main.go; \
	else \
		echo "请安装swag: go install github.com/swaggo/swag/cmd/swag@latest"; \
	fi

# 版本管理
.PHONY: version
version: ## 显示版本信息
	@echo "Agent Gaming Backend v$(VERSION)"

.PHONY: tag
tag: ## 创建版本标签
	@echo "创建版本标签 v$(VERSION)..."
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION) 