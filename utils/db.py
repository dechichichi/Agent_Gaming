import pymysql
import yaml
import os
from contextlib import contextmanager
from typing import Generator, Dict, Any
import logging

logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """加载数据库配置"""
    try:
        # 优先使用环境变量
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'game_agent'),
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'connect_timeout': 30
        }
        
        # 如果环境变量未设置，则从配置文件读取
        if not all([config['host'], config['user'], config['password']]):
            with open('config/config.yml', 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)['DB_CONFIG']
                config.update(file_config)
                
        return config
    except Exception as e:
        logger.error(f"加载数据库配置失败: {str(e)}")
        raise

@contextmanager
def get_db_connection() -> Generator[pymysql.connections.Connection, None, None]:
    """获取数据库连接的上下文管理器"""
    conn = None
    try:
        conn = pymysql.connect(**load_config())
        yield conn
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def execute_query(query: str, params: tuple = None) -> list:
    """执行查询并返回结果"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, params)
                return cursor.fetchall()
            except Exception as e:
                logger.error(f"执行查询失败: {str(e)}\nQuery: {query}\nParams: {params}")
                raise

def execute_update(query: str, params: tuple = None) -> int:
    """执行更新操作并返回影响的行数"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                affected_rows = cursor.execute(query, params)
                conn.commit()
                return affected_rows
            except Exception as e:
                conn.rollback()
                logger.error(f"执行更新失败: {str(e)}\nQuery: {query}\nParams: {params}")
                raise 