
from agents import extract_contents, extract_user_weights, search_listings
from agent_types import State
from langgraph.graph import StateGraph, END
import json


class MasterAgent:
   def __init__(self):
       self.workflow = self._create_workflow()
  
   def _create_workflow(self) -> StateGraph:
       workflow = StateGraph(State)
      
       # nodes
       workflow.add_node("search", search_listings)
       workflow.add_node("extract", extract_contents)
       workflow.add_node("extract_weights", extract_user_weights)
      
       # edges
       workflow.set_entry_point("search")
       workflow.add_edge("search", "extract")
       workflow.add_edge("extract", "extract_weights")
       workflow.add_edge("extract_weights", END)
      
       return workflow.compile()
  
   def run_search(self, query: str) -> dict:
       try:
           initial_state = {"query": query, "urls": [], "raw_contents": [], "top_deals": [], "previous_top_deal": None}
           result = self.workflow.invoke(initial_state)
          
           return {
               "success": True,
               "all_deals": result["top_deals"],
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
  
   result = master.run_search("Apartment for rent in NYC, quiet neighborhood with low crime rate. Budget is $2000-2500 per month. 1 bedroom, 1 bathroom, and in-unit laundry. I really want to live next to my friend in the upper east side. There must be a park nearby and high ceilings.")

   if result['success']:
       print(f"Found {len(result['all_deals'])} cars")
       
       # Save state to file
       with open("state.txt", "w") as f:
           json.dump(result['state'], f, indent=2, default=str)
       print("State saved to state.txt")
   else:
       print(f"Error: {result['error']}")




if __name__ == "__main__":
   main()

