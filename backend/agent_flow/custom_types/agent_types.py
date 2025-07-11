from typing import List
from pydantic import BaseModel

from shared.models import ModifiedRecipeContent, UserInfo

class RawRecipeContent(BaseModel):
   raw_content: str
   page_url: str
   image_urls: List[str] = []


class State(BaseModel):
   is_new_query: bool = False
   user_email: str | None = None
   query_id: str | None = None
   query: str | None = None
   user_info: UserInfo | None = None
   recipe_search_urls: List[str]
   recipe_contents: List[RawRecipeContent]
   modified_recipe_contents: List[ModifiedRecipeContent] = []
   
