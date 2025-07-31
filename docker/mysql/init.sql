-- 创建数据库
CREATE DATABASE IF NOT EXISTS agent_gaming CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agent_gaming;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建用户事件日志表
CREATE TABLE IF NOT EXISTS user_event_log (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    event_time BIGINT NOT NULL,
    event_info TEXT,
    part_date VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_event_time (event_time),
    INDEX idx_part_date (part_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建用户标签表
CREATE TABLE IF NOT EXISTS user_label (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    label_type VARCHAR(20) NOT NULL,
    target INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_label_type (label_type),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建序列输出表
CREATE TABLE IF NOT EXISTS sequential_output (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    train_start_date VARCHAR(20),
    train_end_date VARCHAR(20),
    test_start_date VARCHAR(20),
    test_end_date VARCHAR(20),
    is_prepay INT NOT NULL DEFAULT 0,
    target INT NOT NULL DEFAULT 0,
    part_date VARCHAR(20),
    event_list TEXT,
    stats_item_list TEXT,
    stats_event_list TEXT,
    num_event INT NOT NULL DEFAULT 0,
    max_level INT NOT NULL DEFAULT 0,
    max_viplevel INT NOT NULL DEFAULT 0,
    val_row INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_part_date (part_date),
    INDEX idx_target (target),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建预测模型表
CREATE TABLE IF NOT EXISTS prediction_models (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'training',
    version VARCHAR(20),
    accuracy DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    model_path VARCHAR(255),
    config TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建系统配置表
CREATE TABLE IF NOT EXISTS system_config (
    id VARCHAR(36) PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入默认配置
INSERT INTO system_config (id, config_key, config_value, description) VALUES
(UUID(), 'model_version', '1.0.0', '当前模型版本'),
(UUID(), 'cache_ttl', '3600', '缓存过期时间（秒）'),
(UUID(), 'rate_limit', '100', 'API限流次数（每分钟）'),
(UUID(), 'max_sequence_length', '3000', '最大序列长度'),
(UUID(), 'batch_size', '128', '批处理大小');

-- 创建索引优化查询性能
CREATE INDEX idx_user_event_composite ON user_event_log(user_id, event_time, part_date);
CREATE INDEX idx_sequential_output_composite ON sequential_output(user_id, part_date, target); 