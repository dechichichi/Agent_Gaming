-- 创建 user_event_log 表
CREATE TABLE IF NOT EXISTS user_event_log (
    user_id VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户唯一ID',
    event_time BIGINT(20) NOT NULL COMMENT '用户事件发生的十位时间戳',
    event_name VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户事件的名称',
    part_date VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '日期时间，格式是YYYY-MM-dd',
    event_info TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '用户事件的其他相关信息，JSON类型',
    PRIMARY KEY (event_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='columnar=1' CONNECTION='OSS://xxxx:dxxx@oss-cn-shanghai-internal.aliyuncs.com/xx/xxxx/';