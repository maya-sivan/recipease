from dotenv import load_dotenv
import os
from shared.ssm import get_ssm_parameter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


TAVILY_API_KEY = get_ssm_parameter("tavilyApiKey")
OPENAI_API_KEY = get_ssm_parameter("openAIApiKey")
OPEN_AI_MODEL = os.getenv("OPEN_AI_MODEL")

if(OPEN_AI_MODEL is None):
    logger.warning("OPEN_AI_MODEL is not set, using default model gpt-4.1-nano")
    OPEN_AI_MODEL = "gpt-4.1-nano"
else:
    logger.info(f"OPEN_AI_MODEL is set to {OPEN_AI_MODEL}")

LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = get_ssm_parameter("langsmithAPIKey")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")
