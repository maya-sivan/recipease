from typing import List
from agent_flow.custom_types.agent_types import RawRecipeContent, State
from langchain_openai import ChatOpenAI
from shared.models import ModifiedRecipeContentList
from langchain_core.tools.simple import Tool
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch, TavilyCrawl
from langchain_core.tools import tool


def recipe_modifier_agent(state: State) -> State:
    print("🧠 Recipe Modifier Agent")

    llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
    structured = llm.with_structured_output(ModifiedRecipeContentList, method="function_calling")

    def tavily_search() -> List[str]:
        print("🔍 Searching for recipes")
        if(state.user_info is None):
            raise ValueError("User info is required")
        
        recipe_preferences = ", ".join(state.user_info.preferences) if len(state.user_info.preferences) > 0 else ""
        tool = TavilySearch(
            query=f"Newest {recipe_preferences} recipes with ingredients and instructions",
            max_results=4,
            time_range="day",
            include_domains=["allrecipes.com", "foodnetwork.com", "gimmesomeoven.com"],
        )
        urls = tool.invoke()
        state["recipe_search_urls"] = [res['url'] for res in urls['results']]
        return state["recipe_search_urls"]
    search_tool = Tool.from_function(
        name="tavily_search",
        description="""
            Use this to search for top-level recipe URLs based on user preferences. 
            Use a query like: "Newest {recipe_preferences} recipes with ingredients and instructions".

            Use the following:
            - max_results = 4
            - time_range = "day"
            - include_domains = ["allrecipes.com", "foodnetwork.com", "gimmesomeoven.com"]

            Input: query string
            Output: list of recipe URLs
            """,
        func=tavily_search
    )

    def tavily_crawl() -> List[RawRecipeContent]:
        print("🕸️ Crawling URLs")
        all_recipes: List[RawRecipeContent] = []
        for url in state["recipe_search_urls"]:
            print(f"\tCrawling {url}")
            url_raw_contents = TavilyCrawl(
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
        state["recipe_contents"] = all_recipes
        return state["recipe_contents"]

    crawl_tool = Tool.from_function(
        name="tavily_crawl",
        description="""
            Use this to crawl the recipe URLs obtained from tavily_search.
            Takes a list of recipe page URLs and returns their content.

            Crawl parameters:
            - max_depth = 1
            - max_breadth = 5
            - limit = 3
            - select_paths = ["/recipe/.*", "/recipes/.*"]
            - extract_depth = "basic"
            - include_images = True

            Input: list of URLs
            Output: list of objects with raw_content, page_url, image_urls
            """,
        func=tavily_crawl
    )
    def call_llm(query: str) -> ModifiedRecipeContentList:
        return structured.invoke(query)


    modify_recipe = Tool.from_function(
        func=call_llm,
        name="recipe_modifier_agent",
        description="""
            Use this to select the top 2 easiest-to-modify recipes from a list and rewrite them based on user restrictions.

            Input:
            - recipe_contents: list of {raw_content, page_url, image_urls}
            - user_restrictions: list of strings (e.g. 'no peanuts', 'vegan')
            - user_preferences: list of strings (e.g. 'italian', 'spicy', 'pasta')

            The tool will:
            - Choose the 2 most modifiable recipes
            - Substitute ingredients based on restrictions
            - Return a JSON array of exactly 2 objects, each with:
                - original_page_url
                - modified_recipe_content (markdown with only Ingredients and Directions, escaped for JSON)
                - notes (explanation of changes)
                - image_url
                - recipe_title (2–5 words)
                - relevant_preferences (subset of user preferences, never restrictions)

            Output: JSON string with the 2 modified recipes
        """,
    )

    prompt = """
        You are a recipe recommendation and modification assistant designed to help users discover and adapt recipes that suit their dietary restrictions and preferences.

        You have access to the following tools:

        ---

        ### 🧰 Tools

        1. **tavily_search**
        - Use this to find new recipes.
        - Input: A string query, such as:  
            `"Newest {recipe_preferences} recipes with ingredients and instructions"`
        - Parameters:  
            - max_results = 4  
            - time_range = "day"  
            - include_domains = ["allrecipes.com", "foodnetwork.com", "gimmesomeoven.com"]
        - Output: A list of recipe URLs.

        2. **crawl_agent**
        - Use this to extract full recipe content from URLs.
        - Input: A list of URLs from tavily_search.
        - Crawl Parameters:  
            - max_depth = 1  
            - max_breadth = 5  
            - limit = 3  
            - select_paths = ["/recipe/.*", "/recipes/.*"]  
            - extract_depth = "basic"  
            - include_images = True
        - Output: A list of objects with `raw_content`, `page_url`, and optional `image_urls`.

        3. **modify_recipe**
        - Use this to select and rewrite the top 2 most adaptable recipes.
        - Input:
            - `recipe_contents`: list of recipe documents with `raw_content`, `page_url`, and `image_urls`
            - `user_restrictions`: list of user restrictions (e.g., "gluten free", "no peanuts")
            - `user_preferences`: list of cuisines, flavors, or ingredients the user enjoys (e.g., "italian", "spicy")
        - Output: A JSON array of **exactly 2** modified recipes with:
            - `original_page_url`
            - `modified_recipe_content` (Markdown with **only** "## Ingredients" and "## Directions", escaped for JSON - newlines (\\n) and double quotes (\\"))
            - `notes` explaining substitutions
            - `image_url`
            - `recipe_title` (2–5 words)
            - `relevant_preferences` (subset of input user preferences only; do not include restrictions)

        ---

        ### 🧠 Your Task Flow

        Given:
        - `user_restrictions`: list of dietary restrictions or allergies.
        - `user_preferences`: list of preferred cuisines, ingredients, flavors, or meal types.

        Your steps:
        1. Call the `tavily_search` tool using this query to find candidate recipe URLs.

        2. Call the `crawl_agent` tool with the resulting URLs to fetch the raw recipe content.

        4. Call the `modify_recipe` tool with the crawled recipe content, user restrictions, and user preferences.

        5. Output ONLY the result returned from `modify_recipe` — no explanations or commentary.

        ---

        ### ⚠️ Important Behavior Rules

        - Never guess recipe content — always retrieve it using `tavily_search` and `crawl_agent`.
        - Do not call `modify_recipe` until you have valid `raw_content` and `page_url` for at least 2 recipes.
        - `relevant_preferences` in the final result must only include values from user preferences, never from restrictions.
        - The output of `modify_recipe` must be valid JSON, parsable with `json.loads()`.

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
    """

    agent = create_react_agent(
        model=llm,
        tools=[modify_recipe, search_tool, crawl_tool],
        prompt=prompt,
        response_format=("result", ModifiedRecipeContentList),
        state_schema=State,
    )

    result_state = agent.invoke(state)
    print(result_state)
    recipe_contents: ModifiedRecipeContentList = result_state["structured_response"]
    state["modified_recipe_contents"] = recipe_contents.modified_recipe_contents
    return state

