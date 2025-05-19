import unittest
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from utils.tools import Tools

class TestTools(unittest.TestCase):
    """工具类测试"""
    
    def setUp(self):
        """测试前准备"""
        self.tools = Tools()
        self.user_id = 'test_user'
        self.start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        
    def test_get_user_data(self):
        """测试获取用户数据"""
        data = self.tools.get_user_data(self.user_id, self.start_date, self.end_date)
        self.assertIsInstance(data, pd.DataFrame)
        
    def test_get_user_metrics(self):
        """测试获取用户指标"""
        metrics = self.tools.get_user_metrics(self.user_id)
        self.assertIsInstance(metrics, dict)
        
    def test_get_risk_assessment(self):
        """测试获取风险评估"""
        assessment = self.tools.get_risk_assessment(self.user_id)
        self.assertIsInstance(assessment, dict)
        self.assertIn('risk_level', assessment)
        self.assertIn('risk_score', assessment)
        self.assertIn('metrics', assessment)
        
    def test_get_retention_analysis(self):
        """测试获取留存分析"""
        analysis = self.tools.get_retention_analysis(self.user_id)
        self.assertIsInstance(analysis, dict)
        
    def test_get_user_recommendations(self):
        """测试获取用户推荐"""
        recommendations = self.tools.get_user_recommendations(self.user_id)
        self.assertIsInstance(recommendations, list)
        
        if recommendations:
            recommendation = recommendations[0]
            self.assertIn('type', recommendation)
            self.assertIn('priority', recommendation)
            self.assertIn('action', recommendation)
            self.assertIn('description', recommendation)
            
if __name__ == '__main__':
    unittest.main() 