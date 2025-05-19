import pandas as pd
import numpy as np
from typing import List, Dict, Any, Union
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def preprocess_sequence_data(data: pd.DataFrame) -> pd.DataFrame:
    """统一的数据预处理函数"""
    try:
        # 处理序列数据
        data['event_list'] = data['event_list'].apply(lambda x: [int(i) for i in x.split(',')])
        data['stats_item_list'] = data['stats_item_list'].apply(lambda x: [int(i) for i in x.split(',')])
        data['stats_event_list'] = data['stats_event_list'].apply(lambda x: [int(i) for i in x.split(',')])
        
        # 处理时间戳
        if 'event_time' in data.columns:
            data['event_time'] = pd.to_datetime(data['event_time'], unit='s')
            
        # 处理数值型特征
        numeric_columns = ['max_level', 'max_viplevel', 'num_event']
        for col in numeric_columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
                
        return data
    except Exception as e:
        logger.error(f"数据预处理失败: {str(e)}")
        raise

def extract_time_features(data: pd.DataFrame) -> pd.DataFrame:
    """提取时间特征"""
    try:
        if 'event_time' in data.columns:
            data['hour'] = data['event_time'].dt.hour
            data['day_of_week'] = data['event_time'].dt.dayofweek
            data['is_weekend'] = data['day_of_week'].isin([5, 6]).astype(int)
        return data
    except Exception as e:
        logger.error(f"时间特征提取失败: {str(e)}")
        raise

def calculate_user_metrics(data: pd.DataFrame) -> Dict[str, Any]:
    """计算用户行为指标"""
    try:
        metrics = {
            'total_events': len(data),
            'unique_events': data['event_name'].nunique(),
            'avg_events_per_day': len(data) / (data['event_time'].max() - data['event_time'].min()).days,
            'most_common_event': data['event_name'].mode().iloc[0],
            'active_hours': data['event_time'].dt.hour.value_counts().to_dict()
        }
        return metrics
    except Exception as e:
        logger.error(f"用户指标计算失败: {str(e)}")
        raise

def get_time_range_data(data: pd.DataFrame, time_range: str) -> pd.DataFrame:
    """获取指定时间范围的数据"""
    try:
        end_date = datetime.now()
        if time_range == "week":
            start_date = end_date - timedelta(days=7)
        elif time_range == "month":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=1)
            
        mask = (data['event_time'] >= start_date) & (data['event_time'] <= end_date)
        return data[mask]
    except Exception as e:
        logger.error(f"时间范围数据获取失败: {str(e)}")
        raise

def normalize_features(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """特征标准化"""
    try:
        for col in columns:
            if col in data.columns:
                mean = data[col].mean()
                std = data[col].std()
                data[col] = (data[col] - mean) / std
        return data
    except Exception as e:
        logger.error(f"特征标准化失败: {str(e)}")
        raise 