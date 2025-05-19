from utils.tools import Tools
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """工具类使用示例"""
    try:
        # 初始化工具类
        tools = Tools()
        
        # 测试用户ID
        user_id = 'test_user_001'
        
        # 获取用户指标
        logger.info(f"获取用户 {user_id} 的指标...")
        metrics = tools.get_user_metrics(user_id)
        logger.info(f"用户指标: {metrics}")
        
        # 获取风险评估
        logger.info(f"获取用户 {user_id} 的风险评估...")
        risk_assessment = tools.get_risk_assessment(user_id)
        logger.info(f"风险评估: {risk_assessment}")
        
        # 获取留存分析
        logger.info(f"获取用户 {user_id} 的留存分析...")
        retention_analysis = tools.get_retention_analysis(user_id)
        logger.info(f"留存分析: {retention_analysis}")
        
        # 获取用户推荐
        logger.info(f"获取用户 {user_id} 的推荐...")
        recommendations = tools.get_user_recommendations(user_id)
        logger.info(f"用户推荐: {recommendations}")
        
    except Exception as e:
        logger.error(f"示例运行失败: {str(e)}")
        raise

if __name__ == '__main__':
    main() 