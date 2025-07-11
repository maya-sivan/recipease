from ..helpers.utils import convert_str_to_object_id
from shared.models import Recipe
from fastapi import APIRouter, Request, HTTPException, status
from typing import List



recipe_router = APIRouter()

@recipe_router.get("/all", response_description="List all recipes", response_model=List[Recipe])
def list_recipes(request: Request):
    recipes = list(request.app.database["recipes"].find(limit=3))
    return recipes

@recipe_router.get("/{id}", response_description="Get a single recipe by id", response_model=Recipe)
def find_recipe(id: str, request: Request):
    obj_id = convert_str_to_object_id(id)
    if (recipe := request.app.database["recipes"].find_one({"_id": obj_id})) is not None:
        return recipe
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with ID {id} not found")

