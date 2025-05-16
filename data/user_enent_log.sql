-- 创建 user_event_log，OSS 地址需要配置为正确地址，同一个数据库执行一次即可
CREATE TABLE `user_event_log` (
  `user_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户唯一ID',
  `event_time` bigint(20) NOT NULL COMMENT '用户事件发生的十位时间戳',
  `event_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户事件的名称，比如反映用户付费的行为（是否付费、付费金额等）',
  `part_date` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '日期时间，格式是YYYY-MM-dd',
  `event_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '用户事件的其他相关信息，JSON类型（付费行为的子类型、付费金额等）',
  PRIMARY KEY (`event_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='columnar=1' CONNECTION='OSS://xxxx:dxxx@oss-cn-shanghai-internal.aliyuncs.com/xx/xxxx/'