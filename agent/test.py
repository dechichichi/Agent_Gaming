from typing import Dict, Optional, List
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import BaseChatModel
from agent import GameUserAgent
from tools import tools
from prompt import GAME_USER_ANALYSIS_PROMPT, RETENTION_PLAN_PROMPT

# 创建Agent实例
agent = GameUserAgent(
    tools=tools,
    prompt=GAME_USER_ANALYSIS_PROMPT,
    final_prompt=RETENTION_PLAN_PROMPT
)

# 分析用户风险
user_data = {
    "max_level": 50,
    "max_viplevel": 3,
    "num_event": 100,
    "event_list": ["login", "purchase", "battle", "logout"]
}
risk_analysis = agent.analyze_user_risk("user123", user_data)

# 生成留存计划
retention_plan = agent.generate_retention_plan("user123", "high")

def test_user_risk_analysis():
    """测试用户风险分析"""
    # 创建Agent实例
    agent = GameUserAgent(
        tools=tools,
        prompt=GAME_USER_ANALYSIS_PROMPT,
        final_prompt=RETENTION_PLAN_PROMPT
    )

    # 测试用例1：高风险用户
    high_risk_user = {
        "max_level": 50,
        "max_viplevel": 1,
        "num_event": 30,
        "event_list": ["login", "logout", "login", "logout"]
    }
    result1 = agent.analyze_user_risk("user001", high_risk_user)
    print("\n高风险用户分析结果:")
    print(result1)

    # 测试用例2：中等风险用户
    medium_risk_user = {
        "max_level": 45,
        "max_viplevel": 2,
        "num_event": 60,
        "event_list": ["login", "purchase", "battle", "logout"]
    }
    result2 = agent.analyze_user_risk("user002", medium_risk_user)
    print("\n中等风险用户分析结果:")
    print(result2)

    # 测试用例3：低风险用户
    low_risk_user = {
        "max_level": 60,
        "max_viplevel": 4,
        "num_event": 120,
        "event_list": ["login", "purchase", "battle", "purchase", "battle", "logout"]
    }
    result3 = agent.analyze_user_risk("user003", low_risk_user)
    print("\n低风险用户分析结果:")
    print(result3)

def test_retention_plan():
    """测试留存计划生成"""
    # 创建Agent实例
    agent = GameUserAgent(
        tools=tools,
        prompt=GAME_USER_ANALYSIS_PROMPT,
        final_prompt=RETENTION_PLAN_PROMPT
    )

    # 测试不同风险等级的留存计划
    risk_levels = ["high", "medium", "low"]
    for level in risk_levels:
        result = agent.generate_retention_plan(f"user_{level}", level)
        print(f"\n{level}风险等级的留存计划:")
        print(result)

if __name__ == "__main__":
    print("开始测试用户风险分析...")
    test_user_risk_analysis()
    
    print("\n开始测试留存计划生成...")
    test_retention_plan()