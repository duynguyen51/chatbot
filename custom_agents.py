from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import QueryEngineTool

from tools.sql_tool import football_sql_tool
from tools.general_question import general_tool
from tools.airline_tool import airline_historical_tools, airline_history_retrieve, airline_delay_analyzer
from llm import LLM_MODEL

from typing import List, Literal


def get_openai_agent(tools: List[QueryEngineTool]) -> OpenAIAgent:
    tools = [tool for tool in tools]
    return OpenAIAgent.from_tools(
        tools, llm=LLM_MODEL, verbose=True,
    )


def get_agent(agent_name: Literal["openai"]):
    tools = [airline_historical_tools, airline_history_retrieve, airline_delay_analyzer, football_sql_tool, general_tool]
    if agent_name == "openai":
        return get_openai_agent(tools)
    else:
        raise ValueError(f"Agent {agent_name} not found")
