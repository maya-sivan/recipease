from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator


class UserInfo(BaseModel):
   preferences: List[str] = []
   restrictions: List[str] = []


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


class Query(BaseModel):
   user_email: str
   query: str
   user_info: UserInfo
   created_at: datetime


class Recipe(BaseModel):
    query_id: str
    recipe_content: ModifiedRecipeContent
    restrictions: List[str]
    found_at: datetime