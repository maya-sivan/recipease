from datetime import datetime
from typing import List
from pydantic import BaseModel

from custom_types.agent_types import ModifiedRecipeContent, UserInfo

class Query(BaseModel):
   user_email: str
   query: str
   user_info: UserInfo
   created_at: datetime



class Recipe(BaseModel):
    query_id: str
    recipe_content: ModifiedRecipeContent
    relevant_preferences: List[str]
    restrictions: List[str]
    found_at: datetime