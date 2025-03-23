from langchain.chat_models import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import tomllib
import os

with open("secrets.toml", "rb") as f:
    config = tomllib.load(f)

openai_api_key = config["env"]["OPENAI_API_KEY"]
anthropic_api_key = config["env"]["ANTHROPIC_API_KEY"]

llm = ChatOpenAI(openai_api_key = openai_api_key, 
                 temperature = 0.2,
                 model_name = "gpt-4o")
claude = ChatAnthropic(model="claude-3-opus-20240229",
                       temperature=0.2,
                       anthropic_api_key = anthropic_api_key)