from typing import Any, List
from agent_flow.custom_types.agent_types import RawRecipeContent, State
from langchain_openai import ChatOpenAI
from shared.models import ModifiedRecipeContentList
from langchain_core.tools.simple import Tool
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch, TavilyCrawl
from langchain_core.tools import tool
from agent_flow.setup import OPEN_AI_MODEL
import logging

def recipe_modifier_agent(state: State) -> State:
    print("🧠 Recipe Modifier Agent")

    llm = ChatOpenAI(model=OPEN_AI_MODEL, temperature=0)
    structured = llm.with_structured_output(ModifiedRecipeContentList, method="function_calling")
    
    @tool
    def tavily_search(queries: List[str]) -> List[str]:
        """
        Use this to search for recipe URLs. Input should be a concise query string.
        """
        print(f"🔍 Searching for recipes")
        all_urls = []
        # for query in queries:
        #     print(f"\t🔍 Searching for recipes with query: '{query}'")
        #     search_tool = TavilySearch(
        #         max_results=2,
        #         search_depth="advanced",
        #         exclude_domains=["facebook.com", "instagram.com", "x.com", "youtube.com", "tiktok.com", "snapchat.com", "pinterest.com"], # These domains usually don't have official textual recipes
        #     )
        #     try:
        #         search_results = search_tool.invoke({"query": query})
        #         urls = [res.get("url", "") for res in search_results.get("results", [])]
        #     except Exception as e:
        #         logging.warning(f"Error searching for recipes with query: '{query}': {e}")
        #         urls = []
        #         continue
        # all_urls.extend(urls)
        all_urls = [
        "https://www.allrecipes.com/recipe/45396/easy-pancakes/",
        ]
        return all_urls


    @tool
    def tavily_crawl(urls: List[str]) -> List[RawRecipeContent]:
        """
        Use this to crawl the list of recipe URLs obtained from tavily_search.
        Takes a list of recipe page URLs and returns their content.
        """
        print(f"🕸️ Crawling {len(urls)} URLs one at a time...")
        if(len(urls) == 0):
            logging.warning(f"No URLs to crawl")
            return []

        all_recipes: List[RawRecipeContent] = []

        for url in urls:
            print(f"\tCrawling {url}")
            crawl_tool = TavilyCrawl(
                instructions="recipe pages",
                max_depth=2,
                max_breadth=5,
                limit=10,
                extract_depth="basic",
                include_images=True,
            )
            try:
                url_raw_contents = crawl_tool.invoke({"url": url})
                url_content_result = url_raw_contents.get("results", [])
            except Exception as e:
                logging.warning(f"Error crawling {url}: {e}")
                continue

            for entry in url_content_result:
                rc = RawRecipeContent(
                    raw_content=entry.get("raw_content", ""),
                    page_url=entry.get("url", ""),
                    image_urls=entry.get("images", []) or []
                )
                all_recipes.append(rc)
        return all_recipes

    def call_llm(recipe_contents: List[RawRecipeContent]) -> ModifiedRecipeContentList:
        print(f"🔍 Calling LLM with {len(recipe_contents)} recipe contents")
        try:
            preferences = state["user_info"].preferences
            restrictions = state["user_info"].restrictions
            print(f"\tUser info: preferences: {preferences}, restrictions: {restrictions}")
        except Exception as e:
            logging.warning(f"Error getting user info: {e}")

        if(len(recipe_contents) == 0):
            logging.warning(f"No recipe contents to modify")
            return ModifiedRecipeContentList(modified_recipe_contents=[])
        try:
            return structured.invoke({"recipe_contents": recipe_contents, "restrictions": restrictions, "preferences": preferences})
        except Exception as e:
            logging.warning(f"Error calling modify_recipe tool: {e}")
            return ModifiedRecipeContentList(modified_recipe_contents=[])


    modify_recipe = Tool.from_function(
        func=call_llm,
        name="recipe_modifier_agent",
        description="""
            Use this to select the top recipe that have enough content (ingredients, insturctions, image url) and are the easiest-to-modify from a list and rewrite them based on user restrictions.

            Input:
            - recipe_contents: list of {raw_content, page_url, image_urls}
            - restrictions: list of strings (e.g. 'no peanuts', 'vegan')
            - preferences: list of strings (e.g. 'italian', 'spicy', 'pasta')

            The tool will:
            - Choose a recipe that adehres to one of the values in {preferences} and can be best modified according to {restrictions}
            - Substitute ingredients based on restrictions
            - Return a JSON array of exactly 1 object with:
                - original_page_url
                - modified_recipe_content (markdown escaped for JSON with only Ingredients and Directions (each section titled as ##Ingredients and ##Directions respectively))
                - notes (explanation of changes)
                - image_url (from the raw_content or image_urls - must point to a real, valid URL)
                - recipe_title (2–5 words)
                - relevant_preferences (subset of {preferences}, never contains any values from {restrictions}, never new values)

            Output: JSON string with the 1 modified recipe
        """,
    )

    prompt = """
        You are a recipe recommendation and modification assistant designed to help users discover and adapt recipes that suit their dietary restrictions and preferences.

        You are given a state object that contains the following fields:
            - `user_info`: a UserInfo object with the following fields:
                - `restrictions`: list of dietary restrictions or allergies.
                - `preferences`: list of preferred cuisines, ingredients, flavors, or meal types.
       
        You have access to the following tools:

        ---

        ### 🧰 Tools

        1. **tavily_search**
        - Use this to find potential recipe pages.
        - Input: A list of string queries, each query corresponding to an element in {preferences} (NOT {restrictions}), with this exact format:  
            `["latest {preferences[0]} recipes", "latest {preferences[1]} recipes", ...]`
        - Parameters:  
            - max_results = 10  
            - search_depth = "advanced"  
            - exclude_domains = ["facebook.com", "instagram.com", "x.com", "youtube.com", "tiktok.com", "snapchat.com", "pinterest.com"]
        - Output: A combined list of recipe URLs from ALL the searches.

        2. **tavily_crawl**
        - Use this to specify the search and extract full recipe content from URLs.
        - Input: A list of ALL URLs returned by the tavily_search tool - do not omit any URLs from the list.
        - Crawl Parameters:  
            - instructions="recipe pages",
            - max_depth=2,
            - max_breadth=5,
            - limit=10,
            - extract_depth="basic",
            - include_images=True,
        - Output: A list of objects with `raw_content`, `page_url`, and optional `image_urls`.

        3. **modify_recipe**
        - Use this to select and rewrite the recipe that could be best adapted to {restrictions} (prioritize valid recipes with enough content) and matches a value in {preferences}.
        - Input:
            - `recipe_contents`: list of recipe documents with `raw_content`, `page_url`, and `image_urls`
        - Output: A JSON array of **exactly 1** modified recipe with:
            - `original_page_url`
            - `modified_recipe_content` (Markdown with **only** "## Ingredients" and "## Directions", escaped for JSON - newlines (\\n) and double quotes (\\"))
            - `notes` explaining substitutions
            - `image_url` (from the original recipe page - must point to a real, valid URL)
            - `recipe_title` (2–5 words)
            - `relevant_preferences` (subset of {preferences}, NEVER contains any values from {restrictions}, NEVER contains values that are not in {preferences})

        ---

        ### 🧠 Your Task Flow

        Given:
        - `state`: a State object that contains the following fields:
            - `user_info`: a UserInfo object with the following fields:
                - `restrictions`: list of dietary restrictions or allergies.
                - `preferences`: list of preferred cuisines, ingredients, flavors, or meal types.

        Your steps:
        1. Call the `tavily_search` tool using the search queries list (based only on {preferences}) to find candidate recipe URLs .

        2. Call the `tavily_crawl` tool with the resulting URL list to fetch the raw recipe content.

        4. Call the `modify_recipe` tool with the crawled recipe content, {restrictions}, and {preferences}.

        5. Output ONLY the result returned from `modify_recipe` — no explanations or commentary.

        ---

        ### ⚠️ Important Behavior Rules

        - NEVER use {restrictions} for the tavily_search tool. ONLY use {preferences}.
        - NEVER call `tavily_crawl` until you have valid URLs from `tavily_search`.
        - Do not call `modify_recipe` until you have valid `raw_content` and `page_url` for at least 1 recipe.
        - `relevant_preferences` in the final result must only include values from {preferences}, never from {restrictions}.
        - The markdown content in `modified_recipe_content` should NOT contain notes and images - these is handled by the `notes` and `image_url` fields in the output. The markdown should **ONLY** contain the ingredients and directions.
        - the original_page_url should be the same as the URL in the `page_url` field of the recipe content from tavily_crawl.
        - You MUST always return 1 recipe.

        ### ✅ Example valid inputs and outputs:

        Input: state = {
            "user_info": {
                "restrictions": ["vegan"],
                "preferences": ["italian", "asian", "chinese"]
            }
        }
        Output:
        [
        {
            "original_page_url": "https://example.com/vegan-pasta",
            "modified_recipe_content": "## Ingredients\\n- 1 cup oat milk\\n- 1 tbsp olive oil\\n\\n## Directions\\n1. Heat oil...\\n2. Add pasta...",
            "notes": "Replaced dairy with oat milk and removed butter to accommodate a vegan restriction.",
            "image_url": "https://example.com/images/vegan-pasta.jpg",
            "recipe_title": "Vegan Creamy Pasta",
            "relevant_preferences": ["italian"]
        },
        ]
    """

    agent = create_react_agent(
        model=llm,
        tools=[tavily_search, tavily_crawl, modify_recipe],
        prompt=prompt,
        response_format=("result", ModifiedRecipeContentList),
        state_schema=State,
    )

    result_state = agent.invoke(state)
    recipe_contents: ModifiedRecipeContentList = result_state["structured_response"]
    state["modified_recipe_contents"] = recipe_contents.modified_recipe_contents
    return state


