import logging
import os
from datetime import datetime
from typing import Optional

def setup_logger(name: str, log_dir: str = 'logs', level: int = logging.INFO) -> logging.Logger:
    """设置日志记录器"""
    # 创建日志目录
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # 创建日志文件名
    log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """获取日志记录器"""
    return logging.getLogger(name or __name__)

# 设置默认日志记录器
default_logger = setup_logger('game_agent') 