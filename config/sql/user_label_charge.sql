-- 创建 user_label_charge 表
CREATE TABLE IF NOT EXISTS user_label_charge (
    user_id VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
    target INT
);