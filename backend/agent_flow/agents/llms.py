from ..custom_types.agent_types import State
from shared.models import ModifiedRecipeContent, UserInfo
import json
import openai



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


def recipe_modifier_agent(state: State) -> State:
    print("🧠 LLM #2: Modifying recipes")

    if(state.user_info is None):
      raise ValueError("User info is required")

    system_prompt = """
      You are a recipe modification assistant.

      You are given:
      - A list of RecipeContent objects, each with:
      - raw_content: raw webpage text of a recipe
      - page_url: the URL of the recipe
      - image_urls: optional image URLs
      - A list of user restrictions (e.g., allergies, diets, ingredient exclusions)
      - A list of user preferences (e.g., cuisines, flavors, ingredients they like, or preferred meal time)

      Your task is to:
      1. Identify the top 2 recipes that are easiest to modify while keeping their core structure, taste, and purpose.
      2. Modify those 2 recipes to fully comply with user restrictions by substituting (not removing) problematic ingredients.
      3. Return a valid **JSON array** of **exactly 2 objects**, each representing one modified recipe.

      ---

      ### 🔒 Output Format (Strict)

      Each object **must** have all of these fields (and **no others**):

      {
      "original_page_url": "<string>",                  // Must match the input page_url
      "modified_recipe_content": "<escaped Markdown string>", // Contains only ingredients and directions
      "notes": "<string>",                              // Summary of changes (what and why)
      "image_url": "<string>",                          // Best image from image_urls or from raw_content
      "recipe_title": "<string>",                       // Use title from raw_content or make one (2–5 words)
      "relevant_preferences": ["<string>", ...]         // Subset of input user preferences that apply (most likely a single value)
      }

      ### 🧾 modified_recipe_content Markdown Must Follow This:
      - Only include sections for ## Ingredients and ## Directions
      - Do **not** include title, notes, images, or preferences in the markdown
      - Escape newlines (\\n) and double quotes (\\") for JSON compatibility

      ---

      ### ✅ Example Valid Output (JSON-parsable string):

      [
      {
         "original_page_url": "https://example.com/vegan-pasta",
         "modified_recipe_content": "## Ingredients\\n- 1 cup oat milk\\n- 1 tbsp olive oil\\n\\n## Directions\\n1. Heat oil...\\n2. Add pasta...",
         "notes": "Replaced dairy with oat milk and removed butter to accommodate a vegan restriction.",
         "image_url": "https://example.com/images/vegan-pasta.jpg",
         "recipe_title": "Vegan Creamy Pasta",
         "relevant_preferences": ["italian"]
      },
      {
         "original_page_url": "https://example.com/tofu-stirfry",
         "modified_recipe_content": "## Ingredients\\n- 1 block firm tofu\\n- 2 tbsp soy sauce\\n\\n## Directions\\n1. Press tofu...\\n2. Stir-fry with veggies...",
         "notes": "Used tofu instead of chicken to match vegetarian and dairy-free restrictions.",
         "image_url": "https://example.com/images/tofu-stirfry.jpg",
         "recipe_title": "Tofu Veggie Stir-Fry",
         "relevant_preferences": ["asian", "chinese"]
      }
      ]

      ---

      ### ⚠️ Important Rules

      - Do not add extra fields or sections
      - Do not include headings like "Notes", "Image", or "Recipe Title" inside the markdown
      - You must escape all content correctly so it can be parsed with json.loads()
      - Only include recipes that can be reasonably adapted with substitutions
      - 🔥 **Strict Rule**: relevant_preferences must be a subset of the user preferences only.
         ❌ Do NOT include any user restrictions (like "gluten free", "vegan", "no peanuts", etc.) in relevant_preferences.
         Only include preferences such as cuisines or ingredients the user likes (e.g., "pasta", "pizza", "spicy", "italian").
      - The output must contain ALL the required keys (original_page_url, modified_recipe_content, notes, image_url, recipe_title, relevant_preferences)

      Output only the JSON array. Nothing else.
      """



    user_content = f"""
      Here is the input data.

      User restrictions:
      {json.dumps(state.user_info.restrictions, indent=2)}

      User preferences:
      {json.dumps(state.user_info.preferences, indent=2)}

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
    
    try:
        raw_results = json.loads(content)
        results = [ModifiedRecipeContent.model_validate(result) for result in raw_results]
    except Exception as e:
        print(f"⚠️ Failed to parse LLM output: {e}")
        print(f"LLM #2 Content: {content}")
        raise
   
    state.modified_recipe_contents = results
    return state