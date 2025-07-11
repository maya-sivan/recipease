from ..helpers.utils import convert_str_to_object_id
from shared.models import Query
from fastapi import APIRouter, Request, HTTPException, status
from typing import List

query_router = APIRouter()

@query_router.get("/all", response_description="List all queries", response_model=List[Query])
def list_queries(request: Request):
    queries = list(request.app.database["queries"].find(limit=3))
    return queries

@query_router.get("/{id}", response_description="Get a single query by id", response_model=Query)
def find_query(id: str, request: Request):
    obj_id = convert_str_to_object_id(id)
    if (query := request.app.database["queries"].find_one({"_id": obj_id})) is not None:
        return query
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Query with ID {id} not found")