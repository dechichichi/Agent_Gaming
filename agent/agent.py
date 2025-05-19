# agent/agent.py
from typing import Dict, Optional, List, Tuple
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import BaseChatModel
from langchain.memory import ConversationTokenBufferMemory
from langchain.schema.output_parser import StrOutputParser
from pydantic import ValidationError
import json

from .tools import Action
from .prompt import GAME_USER_ANALYSIS_PROMPT, RETENTION_PLAN_PROMPT

class MyPrintHandler:
    """用于打印中间过程的处理器"""
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(token, end="", flush=True)

class GameUserAgent:
    def __init__(
        self,
        llm: BaseChatModel = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0,
            model_kwargs={"seed": 42}
        ),
        tools=None,
        prompt: str = GAME_USER_ANALYSIS_PROMPT,
        final_prompt: str = RETENTION_PLAN_PROMPT,
        max_thought_steps: Optional[int] = 10,
    ):
        if tools is None:
            tools = []
        self.llm = llm
        self.tools = tools
        self.final_prompt = PromptTemplate.from_template(final_prompt)
        self.max_thought_steps = max_thought_steps
        self.output_parser = PydanticOutputParser(pydantic_object=Action)
        self.prompt = self.__init_prompt(prompt)
        self.llm_chain = self.prompt | self.llm | StrOutputParser()
        self.verbose_printer = MyPrintHandler()

    def __init_prompt(self, prompt):
        """初始化提示词模板"""
        return PromptTemplate.from_template(prompt).partial(
            tools=render_text_description(self.tools),
            format_instructions=self.__chinese_friendly(
                self.output_parser.get_format_instructions(),
            )
        )

    def run(self, task_description: str) -> Dict:
        """Agent主流程"""
        # 思考步数
        thought_step_count = 0

        # 初始化记忆
        agent_memory = ConversationTokenBufferMemory(
            llm=self.llm,
            max_token_limit=4000,
        )
        agent_memory.save_context(
            {"input": "\ninit"},
            {"output": "\n开始"}
        )

        # 开始逐步思考
        while thought_step_count < self.max_thought_steps:
            print(f">>>>Round: {thought_step_count}<<<<")
            action, response = self.__step(
                task_description=task_description,
                memory=agent_memory
            )

            # 如果是结束指令，执行最后一步
            if action.name == "FINISH":
                break

            # 执行动作
            observation = self.__exec_action(action)
            print(f"----\nObservation:\n{observation}")

            # 更新记忆
            self.__update_memory(agent_memory, response, observation)

            thought_step_count += 1

        if thought_step_count >= self.max_thought_steps:
            # 如果思考步数达到上限，返回错误信息
            return {"error": "思考步数达到上限，未能完成任务"}
        else:
            # 否则，执行最后一步
            final_chain = self.final_prompt | self.llm | StrOutputParser()
            reply = final_chain.invoke({
                "task_description": task_description,
                "memory": agent_memory
            })
            return {"result": reply}

    def __step(self, task_description: str, memory) -> Tuple[Action, str]:
        """执行一步思考"""
        response = ""
        for s in self.llm_chain.stream({
            "task_description": task_description,
            "memory": memory
        }, config={
            "callbacks": [
                self.verbose_printer
            ]
        }):
            response += s

        action = self.output_parser.parse(response)
        return action, response

    def __exec_action(self, action: Action) -> str:
        """执行动作"""
        observation = "没有找到工具"
        for tool in self.tools:
            if tool.name == action.name:
                try:
                    # 执行工具
                    observation = tool.run(action.args)
                except ValidationError as e:
                    # 工具的入参异常
                    observation = (
                        f"Validation Error in args: {str(e)}, args: {action.args}"
                    )
                except Exception as e:
                    # 工具执行异常
                    observation = f"Error: {str(e)}, {type(e).__name__}, args: {action.args}"

        return observation

    def analyze_user_risk(self, user_id: str, user_data: Dict) -> Dict:
        """分析用户风险并生成干预策略"""
        task_description = f"""
        分析用户 {user_id} 的风险状况：
        - 用户等级: {user_data.get('max_level')}
        - VIP等级: {user_data.get('max_viplevel')}
        - 事件数量: {user_data.get('num_event')}
        - 行为序列: {user_data.get('event_list')}
        
        请分析用户风险并生成合适的干预策略。
        """
        
        return self.run(task_description)

    def generate_retention_plan(self, user_id: str, risk_level: str) -> Dict:
        """生成用户留存计划"""
        task_description = f"""
        为用户 {user_id} 生成留存计划：
        - 风险等级: {risk_level}
        
        请生成详细的留存干预计划。
        """
        
        return self.run(task_description)

    @staticmethod
    def __update_memory(agent_memory, response, observation):
        """更新记忆"""
        agent_memory.save_context(
            {"input": response},
            {"output": "\n返回结果:\n" + str(observation)}
        )

    @staticmethod
    def __chinese_friendly(string) -> str:
        """处理中文字符串"""
        lines = string.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('{') and line.endswith('}'):
                try:
                    lines[i] = json.dumps(json.loads(line), ensure_ascii=False)
                except:
                    pass
        return '\n'.join(lines)