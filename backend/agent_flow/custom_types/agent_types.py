from typing import List
from pydantic import BaseModel
from shared.models import ModifiedRecipeContent, UserInfo
from langgraph.prebuilt.chat_agent_executor import AgentStateWithStructuredResponse


class RawRecipeContent(BaseModel):
   raw_content: str
   page_url: str
   image_urls: List[str] = []

class State(AgentStateWithStructuredResponse):
   is_new_query: bool = False
   user_email: str | None = None
   query_id: str | None = None
   query: str | None = None
   user_info: UserInfo | None = None
   modified_recipe_content: ModifiedRecipeContent | None = None
