from typing import List
from agent_types import ModifiedRecipeContent, RecipeContent, State, UserInfo
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
   
   # result = tavily_client.search(
   #    query=f"Newest {recipe_preferences} recipes with ingredients and instructions",
   #    max_results=10,
   #    time_range="day",
   #    include_domains=["allrecipes.com", "foodnetwork.com", "gimmesomeoven.com"],
   # )
   # state.recipe_search_urls = [res['url'] for res in result['results']]

   state.recipe_search_urls = [
    "https://www.allrecipes.com/recipe/280256/super-salsa-burgers/",
    "https://www.allrecipes.com/burger-king-frozen-cotton-candy-cloud-returns-11768513"
  ]

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
      for entry in url_raw_contents['results']:
        rc = RecipeContent(
            raw_content=entry.get("raw_content", ""),
            page_url=entry.get("url", ""),
            image_url=entry.get("images", []) or []
        )
        all_recipes.append(rc)

   state.recipe_contents = all_recipes
   return state


def recipe_modifier_agent(state: State) -> State:
    print("🧠 LLM #2: Modifying recipes")

    if(state.user_info is None):
      raise ValueError("User info is required")

    system_prompt = """
      You are a recipe modification assistant. You are given:
      - A list of RecipeContent objects, each with:
      - raw_content: raw webpage text of a recipe
      - page_url: the URL of the recipe
      - image_url: optional image URLs
      - A list of user restrictions (e.g., allergies, diets, ingredient exclusions)

      Your task:
      1. Identify the top 2 recipes that are easiest to modify while keeping their core intent, taste, and structure.
      2. Modify those recipes to meet the restrictions by replacing problematic ingredients with reasonable alternatives (e.g., dairy -> oat milk).
      3. Return 2 modified recipes in JSON format, each with:
      {
         "original_page_url": "<string>",
         "modified_recipe_content": "<string>", # The modified recipe content in markdown format
         "notes": "<brief explanation of what was changed and why>",
         "image_url": "<list of image URLs>" # same as what you were given in the input data
      }

      Guidelines:
      - Always substitute restricted ingredients rather than removing them.
      - Choose substitutions that maintain the integrity of the original recipe.
      - Adjust instructions as needed to reflect substitutions.
      - Only include recipes that can be reasonably adapted.
      - The modified recipe content should be in markdown format and include only the relevant information.
      """

    user_content = f"""
      Here is the input data.

      User restrictions:
      {json.dumps(state.user_info.restrictions, indent=2)}

      Recipes:
      {[rc.model_dump_json(indent=2) for rc in state.recipe_contents]}
   """

    response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError("No content in response")
    content = content.strip()
    
    print(content)
    try:
        results: List[ModifiedRecipeContent] = json.loads(content)
    except Exception as e:
        print("⚠️ Failed to parse LLM output:", e)
        raise
   
   
    state.modified_recipe_contents = results
    return state
