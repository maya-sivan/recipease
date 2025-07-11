
### Search Agent
from typing import List
from ..setup import tavily_client
from ..custom_types.agent_types import RawRecipeContent, State


def search_recipes(state: State) -> State:
   print(f"🔍 Search Agent")
   if(state.user_info is None):
      raise ValueError("User info is required")

   # It is possible that a user does not have any preferences
   recipe_preferences = ", ".join(state.user_info.preferences) if len(state.user_info.preferences) > 0 else ""
   
   result = tavily_client.search(
      query=f"Newest {recipe_preferences} recipes with ingredients and instructions",
      max_results=4,
      time_range="day",
      include_domains=["allrecipes.com", "foodnetwork.com", "gimmesomeoven.com"],
   )
   state.recipe_search_urls = [res['url'] for res in result['results']]

   return state


### Crawl Agent
def extract_contents(state: State) -> State:
   print(f"📄 Crawl Agent")
   all_recipes: List[RawRecipeContent] = []


   for url in state.recipe_search_urls:
      print(f"\tCrawling {url}")
      url_raw_contents = tavily_client.crawl(
          url=url,
         max_depth=1,
         max_breadth=5,
         limit=3,
         select_paths=["/recipe/.*", "/recipes/.*"],
         extract_depth="basic",
         include_images=True
      )
      for entry in url_raw_contents['results']:
        rc = RawRecipeContent(
            raw_content=entry.get("raw_content", ""),
            page_url=entry.get("url", ""),
            image_urls=entry.get("images", []) or []
        )
        all_recipes.append(rc)

   state.recipe_contents = all_recipes
   return state
