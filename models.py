from langchain.chat_models import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")


llm = ChatOpenAI(openai_api_key = openai_api_key, 
                 temperature = 0.2,
                 model_name = "gpt-4o")
claude = ChatAnthropic(model="claude-3-opus-20240229",
                       temperature=0.2,
                       anthropic_api_key = anthropic_api_key)