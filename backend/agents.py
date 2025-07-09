from agent_types import State
from setup import tavily_client

### 1. Search Agent
def search_listings(state: State) -> State:
   print(f"🔍 Search Agent: Starting search for '{state['query']}'")


   result = tavily_client.search(query=state["query"])
   state["urls"] = [res['url'] for res in result['results']]
   return state


### 2. Extract Agent
def extract_contents(state: State) -> State:
   print(f"📄 Extract Agent: Extracting content from {len(state['urls'])} URLs")
   url_raw_contents = tavily_client.extract(urls=state["urls"])
  
   state["raw_contents"] = [data["raw_content"] for data in url_raw_contents["results"]]
   return state
