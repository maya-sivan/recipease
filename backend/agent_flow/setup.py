from dotenv import load_dotenv
import os
from tavily import TavilyClient
from openai import OpenAI

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

