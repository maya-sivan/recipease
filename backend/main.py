
from agents import extract_contents, search_listings
from agent_types import State
from langgraph.graph import StateGraph, END


class MasterAgent:
   def __init__(self):
       self.workflow = self._create_workflow()
  
   def _create_workflow(self) -> StateGraph:
       workflow = StateGraph(State)
      
       # nodes
       workflow.add_node("search", search_listings)
       workflow.add_node("extract", extract_contents)
      
       # edges
       workflow.set_entry_point("search")
       workflow.add_edge("search", "extract")
       workflow.add_edge("extract", END)
      
       return workflow.compile()
  
   def run_search(self, query: str) -> dict:
       try:
           initial_state = {"query": query, "urls": [], "raw_contents": [], "car_data": [], "previous_top_deal": {"price": 0.0, "mileage": 0, "year": 0, "vin": "", "link": ""}}
           result = self.workflow.invoke(initial_state)
          
           return {
               "success": True,
               "all_deals": result["car_data"]
           }
          
       except Exception as e:
           return {
               "success": False,
               "error": str(e),
               "query": query
           }
  




def main():
   master = MasterAgent()
  
   result = master.run_search("Toyota Camry for sale")


   if result['success']:
       print(f"Found {len(result['all_deals'])} cars")
   else:
       print(f"Error: {result['error']}")




if __name__ == "__main__":
   main()

