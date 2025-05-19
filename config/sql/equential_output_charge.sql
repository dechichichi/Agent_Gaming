-- 创建 sequential_output_charge 表
CREATE TABLE IF NOT EXISTS sequential_output_charge (
    train_start_date DATE,
    train_end_date DATE,
    test_start_date DATE,
    test_end_date DATE,
    user_id VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
    is_prepay INT,
    target INT,
    part_date DATE,
    event_list TEXT,
    stats_item_list TEXT,
    stats_event_list TEXT,
    num_event INT,
    max_level INT,
    max_viplevel INT,
    val_row INT
);
