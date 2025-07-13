from dotenv import load_dotenv
import os

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_MODEL = os.getenv("OPEN_AI_MODEL")

if(OPEN_AI_MODEL is None):
    print("OPEN_AI_MODEL is not set, using default model gpt-4.1-nano")
    OPEN_AI_MODEL = "gpt-4.1-nano"
else:
    print(f"OPEN_AI_MODEL is set to {OPEN_AI_MODEL}")

LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")
