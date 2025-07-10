
from typing import Literal
from agents import extract_contents, query_to_features_agent, recipe_modifier_agent, search_recipes
from agent_types import State, UserInfo
from langgraph.graph import StateGraph, END, START
import json


class MasterAgent:
   def __init__(self):
       self.workflow = self._create_workflow()
  
   def _create_workflow(self) -> StateGraph:
       workflow = StateGraph(State)

       def decide_entry_point(state: State) -> Literal["search_recipes", "query_to_features"]:
            """Determines the entry point based on the presence of user information."""
            return "query_to_features" if state.user_info is None else "search_recipes"

      
       # nodes
       workflow.add_node("query_to_features", query_to_features_agent)
       workflow.add_node("search_recipes", search_recipes)
       workflow.add_node("extract_contents", extract_contents)
       workflow.add_node("recipe_modifier", recipe_modifier_agent)
       # edges
       workflow.set_conditional_entry_point(decide_entry_point)
       workflow.add_edge("query_to_features", "search_recipes")
       workflow.add_edge("search_recipes", "extract_contents")
       workflow.add_edge("extract_contents", "recipe_modifier")
       workflow.add_edge("recipe_modifier", END)
      
       return workflow.compile() 
  
   def run_search(self, user_info: UserInfo | None = None, query: str | None = None) -> dict:
       try:
           initial_state = {"query": query, "user_info": user_info, "recipe_search_urls": [], "recipe_contents": []}
           result = self.workflow.invoke(initial_state)
          
           return {
               "success": True,
               "state": result
           }
          
       except Exception as e:
           return {
               "success": False,
               "error": str(e),
               "query": query
           }
  




def main():
   master = MasterAgent()
  
#    result = master.run_search(query="I like unique burgers, Chinese food, and Italian food. I'm allergic to peanuts and need gluten-free recipes.")
   result = master.run_search(user_info=UserInfo(preferences=["unique burgers", "Chinese food", "Italian food"], restrictions=["peanuts", "gluten-free"]))

   if result['success']:
       print(result['state'].modified_recipe_contents)
       # Save state to file
       with open("final_results.txt", "w") as f:
           f.write(result['state'].model_dump_json(indent=2))
       print("State saved to final_results.txt")
   else:
       print(f"Error: {result['error']}")




if __name__ == "__main__":
   main()

