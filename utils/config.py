import os
import yaml
from typing import Dict, Any
import logging
from .logger import get_logger

logger = get_logger(__name__)

def load_config(config_path: str = 'config/config.yml') -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        Dict[str, Any]: 配置字典
    """
    try:
        if not os.path.exists(config_path):
            logger.error(f"配置文件不存在: {config_path}")
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        # 替换环境变量
        config = _replace_env_vars(config)
        
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        raise

def _replace_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    替换配置中的环境变量
    
    Args:
        config: 配置字典
        
    Returns:
        Dict[str, Any]: 替换后的配置字典
    """
    if isinstance(config, dict):
        return {k: _replace_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [_replace_env_vars(item) for item in config]
    elif isinstance(config, str) and config.startswith('${') and config.endswith('}'):
        env_var = config[2:-1]
        value = os.getenv(env_var)
        if value is None:
            logger.warning(f"环境变量未设置: {env_var}")
            return config
        return value
    return config

def get_db_config() -> Dict[str, Any]:
    """
    获取数据库配置
    
    Returns:
        Dict[str, Any]: 数据库配置
    """
    config = load_config()
    return config.get('DB_CONFIG', {})

def get_model_config(model_name: str) -> Dict[str, Any]:
    """
    获取模型配置
    
    Args:
        model_name: 模型名称
        
    Returns:
        Dict[str, Any]: 模型配置
    """
    config = load_config()
    return config.get('MODEL_CONFIG', {}).get(model_name, {})

def get_agent_config() -> Dict[str, Any]:
    """
    获取Agent配置
    
    Returns:
        Dict[str, Any]: Agent配置
    """
    config = load_config()
    return config.get('AGENT_CONFIG', {})

def get_log_config() -> Dict[str, Any]:
    """
    获取日志配置
    
    Returns:
        Dict[str, Any]: 日志配置
    """
    config = load_config()
    return config.get('LOG_CONFIG', {}) 