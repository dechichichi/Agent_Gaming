# agent/tools.py
from typing import List, Dict, Optional
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
import pymysql
import yaml
from datetime import datetime, timedelta

# 加载配置文件
with open('config/config.yml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
DB_CONFIG = config['DB_CONFIG']

class Action(BaseModel):
    """动作模型"""
    name: str = Field(description="动作名称")
    args: Dict = Field(description="动作参数")

def predict_user_churn(
    user_id: str,
    event_list: List[str],
    max_level: int,
    max_viplevel: int,
    num_event: int,
    stats_item_list: List[str],
    stats_event_list: List[str]
) -> Dict:
    """预测用户流失概率"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 调用流失预测模型
        model_name = "GameName_7to14_train_val_lose_20250401_20250430"
        predict_query = f"""
        /*polar4ai*/SELECT user_id,target FROM EVALUATE (MODEL {model_name}, 
        SELECT * FROM sequential_output_lose WHERE user_id = '{user_id}') WITH 
        (x_cols = 'event_list,max_level,max_viplevel,num_event,stats_item_list,stats_event_list',
        y_cols='target',
        s_cols='user_id,target',
        metrics='Fscore');
        """
        cursor.execute(predict_query)
        result = cursor.fetchone()
        
        # 解析结果
        churn_probability = float(result[1]) if result else 0.5
        risk_level = "high" if churn_probability > 0.7 else "medium" if churn_probability > 0.4 else "low"
        
        return {
            "churn_probability": churn_probability,
            "risk_level": risk_level,
            "key_factors": [
                "登录频率下降" if num_event < 50 else "登录频率正常",
                "付费行为减少" if max_viplevel < 2 else "付费行为正常"
            ]
        }
    except Exception as e:
        return {
            "error": str(e),
            "churn_probability": 0.5,
            "risk_level": "unknown",
            "key_factors": []
        }
    finally:
        if 'conn' in locals():
            conn.close()

def analyze_user_behavior(
    user_id: str,
    time_range: str
) -> Dict:
    """分析用户行为模式"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 解析时间范围
        end_date = datetime.now()
        if time_range == "week":
            start_date = end_date - timedelta(days=7)
        elif time_range == "month":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = end_date - timedelta(days=1)
            
        # 查询用户行为数据
        query = f"""
        SELECT 
            event_name,
            event_time,
            JSON_EXTRACT(event_info, '$.activity_type') as activity_type
        FROM user_event_log
        WHERE user_id = '{user_id}'
        AND event_time BETWEEN UNIX_TIMESTAMP('{start_date.strftime('%Y-%m-%d')}')
        AND UNIX_TIMESTAMP('{end_date.strftime('%Y-%m-%d')}')
        ORDER BY event_time
        """
        cursor.execute(query)
        events = cursor.fetchall()
        
        # 分析行为模式
        active_hours = set()
        activities = {}
        for event in events:
            event_time = datetime.fromtimestamp(event[1])
            active_hours.add(f"{event_time.hour:02d}:00-{(event_time.hour+1):02d}:00")
            activity = event[2] or "unknown"
            activities[activity] = activities.get(activity, 0) + 1
            
        # 确定行为模式
        total_events = len(events)
        if total_events > 100:
            behavior_pattern = "hardcore"
        elif total_events > 50:
            behavior_pattern = "regular"
        else:
            behavior_pattern = "casual"
            
        return {
            "behavior_pattern": behavior_pattern,
            "active_hours": sorted(list(active_hours)),
            "preferred_activities": sorted(
                activities.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
        }
    except Exception as e:
        return {
            "error": str(e),
            "behavior_pattern": "unknown",
            "active_hours": [],
            "preferred_activities": []
        }
    finally:
        if 'conn' in locals():
            conn.close()

def generate_intervention_strategy(
    user_id: str,
    risk_level: str
) -> Dict:
    """生成干预策略"""
    strategies = {
        "high": {
            "strategy_type": "urgent_retention",
            "recommended_actions": [
                "发送限时礼包",
                "推送新活动通知",
                "提供专属客服支持",
                "发放VIP体验卡"
            ],
            "priority": "high"
        },
        "medium": {
            "strategy_type": "regular_retention",
            "recommended_actions": [
                "推送新活动通知",
                "发送每日登录奖励",
                "提供游戏攻略"
            ],
            "priority": "medium"
        },
        "low": {
            "strategy_type": "maintenance",
            "recommended_actions": [
                "发送每日登录奖励",
                "推送新版本更新"
            ],
            "priority": "low"
        }
    }
    
    return strategies.get(risk_level, {
        "strategy_type": "unknown",
        "recommended_actions": [],
        "priority": "unknown"
    })

# 创建工具实例
predict_churn_tool = StructuredTool.from_function(
    func=predict_user_churn,
    name="预测用户流失",
    description="基于用户行为数据预测流失概率"
)

analyze_behavior_tool = StructuredTool.from_function(
    func=analyze_user_behavior,
    name="分析用户行为",
    description="分析用户的行为模式和偏好"
)

generate_strategy_tool = StructuredTool.from_function(
    func=generate_intervention_strategy,
    name="生成干预策略",
    description="基于用户风险等级生成干预策略"
)

tools = [predict_churn_tool, analyze_behavior_tool, generate_strategy_tool]