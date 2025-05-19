from sklearn.metrics import f1_score, classification_report, roc_auc_score, precision_recall_curve
import numpy as np
from typing import Dict, Any, Tuple, List
import logging

logger = logging.getLogger(__name__)

def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray = None, 
                  metric: str = 'all') -> Dict[str, Any]:
    """统一的模型评估函数"""
    try:
        results = {}
        
        if metric in ['f1', 'all']:
            results['f1_score'] = f1_score(y_true, y_pred)
            
        if metric in ['classification', 'all']:
            results['classification_report'] = classification_report(y_true, y_pred)
            
        if metric in ['roc_auc', 'all'] and y_prob is not None:
            results['roc_auc_score'] = roc_auc_score(y_true, y_prob)
            
        if metric in ['precision_recall', 'all'] and y_prob is not None:
            precision, recall, thresholds = precision_recall_curve(y_true, y_prob)
            results['precision_recall'] = {
                'precision': precision.tolist(),
                'recall': recall.tolist(),
                'thresholds': thresholds.tolist()
            }
            
        return results
    except Exception as e:
        logger.error(f"模型评估失败: {str(e)}")
        raise

def calculate_risk_score(metrics: Dict[str, Any]) -> float:
    """计算风险分数"""
    try:
        # 定义风险因素及其权重
        risk_factors = {
            'login_frequency': 0.3,
            'payment_behavior': 0.3,
            'activity_level': 0.2,
            'retention_rate': 0.2
        }
        
        # 计算加权风险分数
        risk_score = sum(
            metrics.get(factor, 0) * weight 
            for factor, weight in risk_factors.items()
        )
        
        return min(max(risk_score, 0), 1)  # 归一化到0-1之间
    except Exception as e:
        logger.error(f"风险分数计算失败: {str(e)}")
        raise

def get_risk_level(risk_score: float) -> str:
    """根据风险分数确定风险等级"""
    try:
        if risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.4:
            return "medium"
        else:
            return "low"
    except Exception as e:
        logger.error(f"风险等级确定失败: {str(e)}")
        raise

def calculate_retention_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
    """计算留存相关指标"""
    try:
        metrics = {
            'retention_rate': data.get('retention_rate', 0),
            'churn_probability': data.get('churn_probability', 0),
            'lifetime_value': data.get('lifetime_value', 0),
            'engagement_score': data.get('engagement_score', 0)
        }
        return metrics
    except Exception as e:
        logger.error(f"留存指标计算失败: {str(e)}")
        raise 