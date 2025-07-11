from datetime import datetime
from typing import List
from custom_types.agent_types import ModifiedRecipeContent, UserInfo
from custom_types.entity_types import Query, Recipe
from setup import queries_collection, recipes_collection


def save_query_to_db(query: str, user_info: UserInfo, user_email: str) -> str:
  query_object = Query(
        query=query,
        user_info=user_info,
        created_at=datetime.now(),
        user_email=user_email
  )
  try:
    result = queries_collection.insert_one(query_object.model_dump())
  except Exception as e:
    print(f"Error saving query to db: {e}")
    raise
  print(f"Query saved to db with id: {result.inserted_id}")
  return str(result.inserted_id)


def save_recipes_to_db(query_id: str, recipes: List[ModifiedRecipeContent], restrictions: List[str]) -> None:
    for recipe in recipes:
         recipe_object = Recipe(
            query_id=query_id,
            restrictions=restrictions,
            found_at=datetime.now(),
            recipe_content=recipe
         )
         try:
            result = recipes_collection.insert_one(recipe_object.model_dump())
         except Exception as e:
            print(f"Error saving recipe to db: {e}")
            raise
         print(f"Recipe saved to db with id: {result.inserted_id}")
         