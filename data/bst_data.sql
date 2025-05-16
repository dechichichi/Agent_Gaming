CREATE TABLE `bst_data` (
    `uid`           VARCHAR(255) NOT NULL, 
    `event_list`    TEXT NOT NULL,
    `target`        FLOAT,  -- 选择 FLOAT 作为数据类型
    `val_row`       INT,
    `other_feature` LONGTEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;