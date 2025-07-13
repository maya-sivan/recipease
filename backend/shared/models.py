from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId



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
class ModifiedRecipeContentList(BaseModel):
    modified_recipe_contents: List[ModifiedRecipeContent]

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


class QueryResponse(Query):
    id: str = Field(..., alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            return v
        raise ValueError(f"Invalid ObjectId: {v}")

    class Config:
        json_encoders = {ObjectId: str}


class JobRequest(BaseModel):
    user_email: str
    query: str

class BgJobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class BgJob(BaseModel):
    job_id: str
    status: BgJobStatus
    created_at: datetime
    started_at: datetime
    completed_at: Optional[datetime] = None
    user_email: str
    query: str
    is_resolved: bool = False

class UpdateBgJob(BaseModel):
    class Config:
        all_optional = True


class UpdateResolvedStatus(BaseModel):
    is_user_resolved: bool