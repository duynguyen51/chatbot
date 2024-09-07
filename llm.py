from config import config
from llama_index.llms.openai import OpenAI


__LLM_MODEL_NAME = config["llm"]["model_name"]

LLM_MODEL = OpenAI(model=__LLM_MODEL_NAME)
