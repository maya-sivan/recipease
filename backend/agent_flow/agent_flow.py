
from typing import Literal
from shared.db import queries_collection
from .custom_types.agent_types import State
from shared.models import Query
from langgraph.graph import StateGraph, END
from bson import ObjectId
from .agents.llms import query_to_features_agent, recipe_modifier_agent
from .agents.tavily_api_agents import search_recipes, extract_contents
from .agents.db_agents import save_data_to_db

class MasterAgent:
   def __init__(self):
       self.workflow = self._create_workflow()
  
   def _create_workflow(self) -> StateGraph:
       workflow = StateGraph(State)

       def decide_entry_point(state: State) -> Literal["search_recipes", "query_to_features"]:
            return "query_to_features" if state.is_new_query else "search_recipes"


       # nodes
       workflow.add_node("query_to_features", query_to_features_agent)

       workflow.add_node("search_recipes", search_recipes)
       workflow.add_node("extract_contents", extract_contents)
       workflow.add_node("recipe_modifier", recipe_modifier_agent)
       workflow.add_node("save_data_to_db", save_data_to_db)
       # edges
       workflow.set_conditional_entry_point(decide_entry_point)

       workflow.add_edge("query_to_features", "search_recipes")

       workflow.add_edge("search_recipes", "extract_contents")
       workflow.add_edge("extract_contents", "recipe_modifier")
       workflow.add_edge("recipe_modifier", "save_data_to_db")
       workflow.add_edge("save_data_to_db", END)
      
       return workflow.compile() 

   def run_new_query(self, user_email: str, query: str) -> State:
        print(f"Running new query {query}")
        try: 
            initial_state = State(
                is_new_query=True,
                query_id=None,
                query=query,
                user_info=None,
                recipe_search_urls=[],
                recipe_contents=[],
                user_email=user_email,
            )
            raw_result = self.workflow.invoke(initial_state)
            result = State(**raw_result)
            return result
            
        except Exception as e:
            print(f"Error running new query: {e}")
            raise e
        
   def run_scheduled_query(self, query_id: str) -> State:
        print(f"Running scheduled query {query_id}")
        try: 
            try:
                query_data = queries_collection.find_one({"_id": ObjectId(query_id)})
                saved_data = Query(**query_data)
            except Exception as e:
                print(f"Error finding query in db: {e}")
                raise e

            initial_state = State(
                is_new_query=False,
                query_id=query_id,
                query=saved_data.query,
                user_info=saved_data.user_info,
                recipe_search_urls=[],
                recipe_contents=[],
                user_email=saved_data.user_email,
            )

            raw_result = self.workflow.invoke(initial_state)
            result = State(**raw_result)
            return result
            
        except Exception as e:
            print(f"Error running scheduled query {query_id}: {e}")
            raise e


