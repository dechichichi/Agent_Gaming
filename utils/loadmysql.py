import json
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    'host': 'dechichichi.rwlb.rds.aliyuncs.com',
    'port': 3306,
    'user': 'lyan',
    'password': 'Ly05985481282',
    'database': 'game_agent',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor,
    'connect_timeout': 30
}

# JSON 文件路径
JSON_FILE_PATH = './utils/user_event_log.json'

def create_table_if_not_exists(connection):
    """创建表（如果不存在）"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS user_event_log (
        user_id VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户唯一ID',
        event_time BIGINT(20) NOT NULL COMMENT '用户事件发生的十位时间戳',
        event_name VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户事件的名称',
        part_date VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '日期时间，格式是YYYY-MM-dd',
        event_info TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '用户事件的其他相关信息，JSON类型',
        PRIMARY KEY (event_time)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='columnar=1' CONNECTION='OSS://xxxx:dxxx@oss-cn-shanghai-internal.aliyuncs.com/xx/xxxx/';
    """
    with connection.cursor() as cursor:
        cursor.execute(create_table_sql)
    connection.commit()

def insert_json_data_to_db():
    """将JSON数据插入到数据库"""
    try:
        # 读取JSON文件
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print("JSON文件为空，没有数据可插入")
            return
        
        # 连接数据库
        with pymysql.connect(**DB_CONFIG) as connection:
            # 创建表
            create_table_if_not_exists(connection)
            
            # 准备插入语句
            columns = ["user_id", "event_time", "event_name", "part_date", "event_info"]
            placeholders = ', '.join(['%s'] * len(columns))
            insert_sql = f"INSERT INTO user_event_log ({', '.join(columns)}) VALUES ({placeholders})"
            
            # 批量插入数据
            with connection.cursor() as cursor:
                inserted_count = 0
                for item in data:
                    try:
                        # 修改日期格式
                        item['part_date'] = datetime.strptime(item['part_date'], '%Y/%m/%d').strftime('%Y-%m-%d')  
                        values = [
                            item['user_id'],
                            item['event_time'],
                            item['event_name'],
                            item['part_date'],
                            json.dumps(item['event_info'])  # 将 event_info 转换为 JSON 字符串
                        ]
                        cursor.execute(insert_sql, values)
                        inserted_count += 1
                    except pymysql.MySQLError as e:
                        # 捕获主键冲突错误
                        if e.args[0] == 1062:
                            print(f"跳过重复记录: {item['event_time']}")
                        else:
                            raise  # 重新抛出其他数据库错误
                connection.commit()
                print(f"成功插入 {inserted_count} 条记录到 user_event_log 表")
    
    except FileNotFoundError:
        print(f"错误：找不到文件 {JSON_FILE_PATH}")
    except json.JSONDecodeError:
        print(f"错误：JSON文件格式不正确 {JSON_FILE_PATH}")
    except pymysql.Error as e:
        print(f"数据库错误：{e}")
    except Exception as e:
        print(f"未知错误：{e}")

if __name__ == "__main__":
    insert_json_data_to_db()