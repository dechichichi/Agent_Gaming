import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime, timedelta
import yaml

# 加载配置文件
with open('config/config.yml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
DB_CONFIG = config['DB_CONFIG']

def create_procedure_if_not_exists(cursor, procedure_name, procedure_sql):
    """
    检查存储过程是否存在，如果不存在则创建它
    :param cursor: 数据库游标
    :param procedure_name: 存储过程名称
    :param procedure_sql: 创建存储过程的 SQL 语句
    """
    cursor.execute(f"""
    SELECT ROUTINE_NAME 
    FROM INFORMATION_SCHEMA.ROUTINES 
    WHERE ROUTINE_SCHEMA = DATABASE() 
      AND ROUTINE_TYPE = 'PROCEDURE' 
      AND ROUTINE_NAME = '{procedure_name}'
    """)
    result = cursor.fetchone()
    if not result:
        print(f"存储过程 {procedure_name} 不存在，正在创建...")
        cursor.execute(procedure_sql)
        print(f"存储过程 {procedure_name} 创建成功！")
    else:
        print(f"存储过程 {procedure_name} 已存在，无需创建。")

def generate_training_data():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 存储过程 SQL
    gen_user_label_charge_sql = """
    DROP PROCEDURE IF EXISTS gen_user_label_charge;
    CREATE PROCEDURE gen_user_label_charge(
        IN seq_time_start DATE,
        IN seq_time_end DATE,
        IN label_time_start DATE,
        IN label_time_end DATE
    )
    BEGIN
        CREATE TABLE IF NOT EXISTS user_label_charge (
            user_id VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
            target INT
        );
        TRUNCATE TABLE user_label_charge;
        INSERT INTO user_label_charge (user_id, target)
        SELECT 
            user_id,
            CASE 
                WHEN COUNT(event_name) > 0 THEN 1
                ELSE 0
            END AS target
        FROM user_event_log
        WHERE event_name = 'Money'
          AND event_time BETWEEN UNIX_TIMESTAMP(label_time_start) AND UNIX_TIMESTAMP(label_time_end)
        GROUP BY user_id;
    END;
    """
    gen_sequential_output_charge_sql = """
    DROP PROCEDURE IF EXISTS gen_sequential_output_charge;
    CREATE PROCEDURE gen_sequential_output_charge(
        IN seq_time_start DATE,
        IN seq_time_end DATE,
        IN label_time_start DATE,
        IN label_time_end DATE
    )
    BEGIN
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
        TRUNCATE TABLE sequential_output_charge;
        INSERT INTO sequential_output_charge (
            train_start_date,
            train_end_date,
            test_start_date,
            test_end_date,
            user_id,
            is_prepay,
            target,
            part_date,
            event_list,
            stats_item_list,
            stats_event_list,
            num_event,
            max_level,
            max_viplevel,
            val_row
        )
        SELECT
            seq_time_start AS train_start_date,
            seq_time_end AS train_end_date,
            label_time_start AS test_start_date,
            label_time_end AS test_end_date,
            uel.user_id,
            CASE 
                WHEN COUNT(CASE WHEN uel.event_name = 'Money' THEN 1 END) > 0 THEN 1
                ELSE 0
            END AS is_prepay,
            ulc.target,
            seq_time_start AS part_date,
            GROUP_CONCAT(uel.event_name ORDER BY uel.event_time) AS event_list,
            GROUP_CONCAT(JSON_EXTRACT(uel.event_info, '$.money_type') ORDER BY uel.event_time) AS stats_item_list,
            GROUP_CONCAT(uel.event_name ORDER BY uel.event_time) AS stats_event_list,
            COUNT(*) AS num_event,
            MAX(JSON_EXTRACT(uel.event_info, '$.level')) AS max_level,
            MAX(JSON_EXTRACT(uel.event_info, '$.viplevel')) AS max_viplevel,
            0 AS val_row
        FROM user_event_log uel
        JOIN user_label_charge ulc ON uel.user_id = ulc.user_id
        WHERE uel.event_time BETWEEN UNIX_TIMESTAMP(seq_time_start) AND UNIX_TIMESTAMP(seq_time_end)
        GROUP BY uel.user_id;
    END;
    """
    # 创建存储过程（如果不存在）
    create_procedure_if_not_exists(cursor, "gen_user_label_charge", gen_user_label_charge_sql)
    create_procedure_if_not_exists(cursor, "gen_sequential_output_charge", gen_sequential_output_charge_sql)

    # 数据加工
    start_date = datetime(2025, 4, 1)
    seq_time_start = start_date
    seq_time_end = start_date + timedelta(days=6)
    label_time_start = seq_time_end + timedelta(days=1)
    label_time_end = label_time_start + timedelta(days=6)

    # 生成用户是否充值的标记数据
    gen_label_charge_query = f"CALL gen_user_label_charge('{seq_time_start.strftime('%Y-%m-%d')}', '{seq_time_end.strftime('%Y-%m-%d')}', '{label_time_start.strftime('%Y-%m-%d')}', '{label_time_end.strftime('%Y-%m-%d')}')"
    cursor.execute(gen_label_charge_query)

    # 生成充值场景下的用户行为序列，并关联标记数据
    gen_seq_charge_query = f"CALL gen_sequential_output_charge('{seq_time_start.strftime('%Y-%m-%d')}', '{seq_time_end.strftime('%Y-%m-%d')}', '{label_time_start.strftime('%Y-%m-%d')}', '{label_time_end.strftime('%Y-%m-%d')}')"
    cursor.execute(gen_seq_charge_query)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    generate_training_data()