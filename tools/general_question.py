from llama_index.core.tools import FunctionTool

from llm import LLM_MODEL


def answer_general_question(question: str) -> str:
    """
    Use the LLM to answer general questions not related to the SQL database.
    """
    response = LLM_MODEL.complete(question)
    return response.text


# Create general knowledge tool
general_tool = FunctionTool.from_defaults(
    fn=answer_general_question,
    description="Useful to answer if can not retrieve answer from other tools."
)