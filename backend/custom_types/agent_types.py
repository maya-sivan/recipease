from typing import List
from pydantic import BaseModel


class UserInfo(BaseModel):
   preferences: List[str] = []
   restrictions: List[str] = []

class RawRecipeContent(BaseModel):
   raw_content: str
   page_url: str
   image_urls: List[str] = []

class ModifiedRecipeContent(BaseModel):
   original_page_url: str
   modified_recipe_content: str
   notes: str
   image_url: str | None = None
   recipe_title: str    
   relevant_preferences: List[str]

class State(BaseModel):
   user_email: str | None = None
   query: str | None = None
   user_info: UserInfo | None = None
   recipe_search_urls: List[str]
   recipe_contents: List[RawRecipeContent]
   modified_recipe_contents: List[ModifiedRecipeContent] = []
   
