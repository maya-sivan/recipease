from datetime import datetime
from typing import List
import logging

from shared.db import queries_collection, recipes_collection
from shared.models import ModifiedRecipeContent, UserInfo, Query, Recipe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    logger.error(f"Error saving query to db: {e}")
    raise
  logger.info(f"Query saved to db with id: {result.inserted_id}")
  return str(result.inserted_id)


def save_recipe_to_db(query_id: str, recipe: ModifiedRecipeContent, restrictions: List[str]) -> None:
    recipe_object = Recipe(
      query_id=query_id,
      restrictions=restrictions,
      found_at=datetime.now(),
      recipe_content=recipe
    )
    try:
      result = recipes_collection.insert_one(recipe_object.model_dump())
    except Exception as e:
      logger.error(f"Error saving recipe to db: {e}")
      raise
    logger.info(f"Recipe saved to db with id: {result.inserted_id}")
    