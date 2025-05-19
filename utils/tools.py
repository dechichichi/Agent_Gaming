from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .db import get_db_connection, execute_query, execute_update
from .data_processor import (
    preprocess_sequence_data,
    extract_time_features,
    calculate_user_metrics,
    get_time_range_data,
    normalize_features
)
from .metrics import (
    evaluate_model,
    calculate_risk_score,
    get_risk_level,
    calculate_retention_metrics
)
from .config import get_db_config, get_model_config, get_agent_config, get_log_config
from .logger import get_logger

logger = get_logger(__name__)

class Tools:
    """工具管理类"""
    
    def __init__(self):
        """初始化工具类"""
        self.db_config = get_db_config()
        self.model_config = get_model_config
        self.agent_config = get_agent_config()
        self.log_config = get_log_config()
        
    def get_user_data(self, user_id: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        获取用户数据
        
        Args:
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            pd.DataFrame: 用户数据
        """
        try:
            query = """
                SELECT *
                FROM user_events
                WHERE user_id = %s
                AND event_time BETWEEN %s AND %s
                ORDER BY event_time
            """
            data = execute_query(query, (user_id, start_date, end_date))
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"获取用户数据失败: {str(e)}")
            raise
            
    def get_user_metrics(self, user_id: str, days: int = 7) -> Dict[str, Any]:
        """
        获取用户指标
        
        Args:
            user_id: 用户ID
            days: 天数
            
        Returns:
            Dict[str, Any]: 用户指标
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            data = self.get_user_data(user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            if data.empty:
                return {}
                
            # 预处理数据
            data = preprocess_sequence_data(data)
            data = extract_time_features(data)
            
            # 计算指标
            metrics = calculate_user_metrics(data)
            
            return metrics
        except Exception as e:
            logger.error(f"获取用户指标失败: {str(e)}")
            raise
            
    def get_risk_assessment(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户风险评估
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict[str, Any]: 风险评估结果
        """
        try:
            # 获取用户指标
            metrics = self.get_user_metrics(user_id)
            if not metrics:
                return {'risk_level': 'unknown', 'risk_score': 0.0}
                
            # 计算风险分数
            risk_score = calculate_risk_score(metrics)
            
            # 获取风险等级
            risk_level = get_risk_level(risk_score)
            
            return {
                'risk_level': risk_level,
                'risk_score': risk_score,
                'metrics': metrics
            }
        except Exception as e:
            logger.error(f"获取风险评估失败: {str(e)}")
            raise
            
    def get_retention_analysis(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户留存分析
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict[str, Any]: 留存分析结果
        """
        try:
            # 获取用户数据
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            data = self.get_user_data(user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            
            if data.empty:
                return {}
                
            # 计算留存指标
            retention_metrics = calculate_retention_metrics(data)
            
            return retention_metrics
        except Exception as e:
            logger.error(f"获取留存分析失败: {str(e)}")
            raise
            
    def get_user_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """
        获取用户推荐
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[Dict[str, Any]]: 推荐列表
        """
        try:
            # 获取用户风险评估
            risk_assessment = self.get_risk_assessment(user_id)
            
            # 获取用户留存分析
            retention_analysis = self.get_retention_analysis(user_id)
            
            # 根据风险等级和留存分析生成推荐
            recommendations = []
            
            if risk_assessment['risk_level'] == 'high':
                recommendations.append({
                    'type': 'retention',
                    'priority': 'high',
                    'action': 'immediate_intervention',
                    'description': '用户流失风险高，建议立即干预'
                })
                
            if retention_analysis.get('churn_probability', 0) > 0.7:
                recommendations.append({
                    'type': 'engagement',
                    'priority': 'high',
                    'action': 'increase_engagement',
                    'description': '用户参与度低，建议提高用户参与度'
                })
                
            return recommendations
        except Exception as e:
            logger.error(f"获取用户推荐失败: {str(e)}")
            raise 