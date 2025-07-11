from typing import List
from pydantic import BaseModel, field_validator


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

   @field_validator("original_page_url", "modified_recipe_content", "notes", "recipe_title", mode="before")
   @classmethod
   def ensure_string(cls, v) -> str:
        if v is None:
            return ""
        return str(v)

   @field_validator("relevant_preferences", mode="before")
   @classmethod
   def ensure_list(cls, v) -> List[str]:
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        return v


class State(BaseModel):
   is_new_query: bool = False
   user_email: str | None = None
   query_id: str | None = None
   query: str | None = None
   user_info: UserInfo | None = None
   recipe_search_urls: List[str]
   recipe_contents: List[RawRecipeContent]
   modified_recipe_contents: List[ModifiedRecipeContent] = []
   
