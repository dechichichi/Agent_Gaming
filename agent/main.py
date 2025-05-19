from agent import GameUserAgent
from tools import tools
from prompt import GAME_USER_ANALYSIS_PROMPT, RETENTION_PLAN_PROMPT

agent = GameUserAgent(
    tools=tools,
    prompt=GAME_USER_ANALYSIS_PROMPT,
    final_prompt=RETENTION_PLAN_PROMPT
)

user_data = {
    "max_level": 50,
    "max_viplevel": 3,
    "num_event": 100,
    "event_list": ["login", "purchase", "battle", "logout"]
}
risk_analysis = agent.analyze_user_risk("user123", user_data)

retention_plan = agent.generate_retention_plan("user123", "high")