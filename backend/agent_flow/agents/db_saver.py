from ..custom_types.agent_types import State
from ..helpers.db_utils import save_query_to_db, save_recipe_to_db

def save_data_to_db(state: State) -> State:
      print("💾 Saving data to db")

      if(state["query"] is None):
         raise ValueError("Query is required")
      if(state["user_info"] is None):
         raise ValueError("User info is required")
      if(state["user_email"] is None):
         raise ValueError("User email is required")

      if(state["is_new_query"]):
         state["query_id"] = save_query_to_db(query=state["query"], user_info=state["user_info"], user_email=state["user_email"])

      if(state["query_id"] is None):
         raise ValueError("Query id is required")

      save_recipe_to_db(query_id=state["query_id"], recipe=state["modified_recipe_content"], restrictions=state["user_info"].restrictions)
      return state