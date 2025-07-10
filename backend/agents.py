from typing import List, get_type_hints
from agent_types import RecipeContent, State, UserInfo
from setup import tavily_client
import openai
import json

def query_to_features_agent(state: State) -> State:
    print("🧠 LLM #1: Extracting features from query")

    system_prompt = (
     "You are a friendly recipe assistant. Your task is to parse user-provided food preferences and dietary restrictions.\n\n"
     "- User input may include cuisine types, flavors, ingredients they like, plus allergies, diets, or dislikes.\n\n"
     "- Return a JSON object with exactly two keys: \n"
     "1. \"preferences\": an array of keywords or short descriptions about foods/cuisines/tastes.\n"
     "2. \"restrictions\": an array of keywords or short descriptions about allergies, diets, or ingredients to avoid.\n\n"

     "Output requirements:\n"
     "- Valid JSON only (no extra text).\n"
     "- Each list may be empty, but must be present.\n"
     "- Items should be concise (1–4 words or brief phrases).\n"
     "- Do NOT include recipes—only parse user info.\n\n"

      "Example:\n"

     "User: \"I love spicy Thai and Mexican food, but I'm allergic to peanuts and need gluten-free recipes.\"\n"
     "Output:\n"
     "{\n"
     "  \"preferences\": [\"spicy Thai\", \"Mexican\"],\n"
     "  \"restrictions\": [\"peanut allergy\", \"gluten-free\"]\n"
     "}"
   )

    user_query = state.query
    response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {user_query}"}
        ],
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError("No content in response")
    content = content.strip()

    try:
        results: UserInfo = json.loads(content)
    except Exception as e:
        print("⚠️ Failed to parse LLM output:", e)
        raise
   
   
    state.user_info = results
    return state


### Search Agent
def search_recipes(state: State) -> State:
   print(f"🔍 Search Agent")
   if(state.user_info is None):
      raise ValueError("User info is required")

   # It is possible that a user does not have any preferences
   recipe_preferences = ", ".join(state.user_info.preferences) if len(state.user_info.preferences) > 0 else ""
   
   result = tavily_client.search(
      query=f"Newest {recipe_preferences} recipes with ingredients and instructions",
      max_results=10,
      time_range="day",
      include_domains=["allrecipes.com", "foodnetwork.com", "gimmesomeoven.com"],
   )
   state.recipe_search_urls = [res['url'] for res in result['results']]

   return state


### Crawl Agent
def extract_contents(state: State) -> State:
   print(f"📄 Crawl Agent")
   all_recipes: List[RecipeContent] = []


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
      print(f"\t\t{url_raw_contents['results']}")
      for entry in url_raw_contents['results']:
        rc = RecipeContent(
            raw_content=entry.get("raw_content", ""),
            page_url=entry.get("url", ""),
            image_url=entry.get("images", []) or []
        )
        all_recipes.append(rc)

   state.recipe_contents = all_recipes
   return state


