from ..helpers.exports import recipe_to_text
from api.helpers.utils import convert_str_to_object_id
from shared.models import RecipeResponse
from fastapi import APIRouter, Request, HTTPException, status, Response
from typing import List



recipe_router = APIRouter()

@recipe_router.get("/all", response_description="List all recipes", response_model=List[RecipeResponse])
def list_recipes(request: Request):
    recipes = list(request.app.database["recipes"].find(limit=50))
    return recipes

@recipe_router.get("/{id}", response_description="Get a single recipe by id", response_model=RecipeResponse)
def find_recipe(id: str, request: Request):
    obj_id = convert_str_to_object_id(id)
    if (recipe := request.app.database["recipes"].find_one({"_id": obj_id})) is not None:
        return recipe
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with ID {id} not found")

@recipe_router.get("/by-query/{query_id}", response_description="Get recipes by query id", response_model=List[RecipeResponse])
def find_recipes_by_query_id(query_id: str, request: Request):
    if (recipes := list(request.app.database["recipes"].find({"query_id": query_id}))) is not None:
        return recipes
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipes with query ID {query_id} not found")

@recipe_router.delete("/{id}", response_description="Delete a single recipe by id")
def delete_recipe(id: str, request: Request):
    obj_id = convert_str_to_object_id(id)
    if (recipe := request.app.database["recipes"].delete_one({"_id": obj_id})) is None:
        raise HTTPException(status_code=404, detail=f"Recipe with ID {id} not found")
    return {"recipe_id": id}        


@recipe_router.post("/export/txt", response_class=Response)
async def export_text(recipe: RecipeResponse, request: Request):
    text = recipe_to_text(recipe) 
    file_name = f"{"_".join(recipe.recipe_content.recipe_title.split(" "))}.txt"
    headers = {"Content-Disposition": f'attachment; filename="{file_name}"'}
    return Response(content=text, media_type="text/plain", headers=headers)