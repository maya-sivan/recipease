from typing import Any, List

from langchain_core.prompts import PromptTemplate
from agent_flow.custom_types.agent_types import RawRecipeContent, State
from langchain_openai import ChatOpenAI
from shared.models import ModifiedRecipeContent
from langchain_core.tools.simple import Tool
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch, TavilyCrawl
from langchain_core.tools import tool
from agent_flow.setup import OPEN_AI_MODEL
import logging

def recipe_modifier_agent(state: State) -> State:
    print("🧠 Recipe Modifier Agent")

    if state["user_info"] is None:
        raise ValueError("User info is required")
    
    
    @tool
    def tavily_search(queries: List[str]) -> List[str]:
        """
        Use this to search for recipe URLs. Input should be a concise query string.
        """
        print(f"🔍 Searching for recipes")
        all_urls = []
        for query in queries:
            print(f"\t🔍 Searching for recipes with query: '{query}'")
            search_tool = TavilySearch(
                max_results=5,
                search_depth="advanced",
                exclude_domains=["facebook.com", "instagram.com", "x.com", "youtube.com", "tiktok.com", "snapchat.com", "pinterest.com"], # These domains usually don't have official textual recipes
            )
            try:
                search_results = search_tool.invoke({"query": query})
                urls = [res.get("url", "") for res in search_results.get("results", [])]
            except Exception as e:
                logging.warning(f"Error searching for recipes with query: '{query}': {e}")
                urls = []
                continue
        all_urls.extend(urls)
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
        print(f"🕸️ Finished crawling all recipes")
        return all_recipes

    @tool   
    def modify_recipe(modified_recipe_content: ModifiedRecipeContent) -> ModifiedRecipeContent:
        """
        Use this to validate the modified recipe content.
        Input:
            - modified_recipe_content: ModifiedRecipeContent object
        Output:
            - modified_recipe_content: validated input
        """
        return modified_recipe_content
        
    prompt_template = """
        You are a recipe recommendation and modification assistant designed to help users discover and adapt recipes that suit their dietary restrictions and preferences.

        You are given the following information:
            - `restrictions`:  {restrictions}. It is a list of dietary restrictions or allergies. Example: ["vegan", "gluten-free", "no peanuts"]
            - `preferences`: {preferences}. It is a list of preferred cuisines, ingredients, flavors, or meal types. Example: ["italian", "asian", "chinese"]

        You have access to the following tools:

        ---

        ### 🧰 Tools

        1. **tavily_search**
        - Use this to find potential recipe pages.
        - Input: A list of string queries, each query corresponding to an element in {preferences} (NOT {restrictions}).
        - Parameters:  
            - max_results = 5  
            - search_depth = "advanced"  
            - exclude_domains = ["facebook.com", "instagram.com", "x.com", "youtube.com", "tiktok.com", "snapchat.com", "pinterest.com"]
        - Output: A combined list of recipe URLs from ALL the searches.

        2. **tavily_crawl**
        - Use this to extract full recipe content from URLs.
        - Input: A list of ALL URLs returned by the tavily_search tool — do not omit any URLs from the list.
        - Crawl Parameters:  
            - max_depth = 2  
            - max_breadth = 5  
            - limit = 10  
            - extract_depth = "basic"  
            - include_images = True
        - Output: A list of objects containing the fields: `raw_content`, `page_url`, and `image_urls`.

        3. **modify_recipe**
        - Use this to verify the modified recipe content.
        - Input:
            - modified_recipe_content: ModifiedRecipeContent object
        - Output:
            - modified_recipe_content: validated input

        ---

        ### 🧠 Your Task Flow

        1. Call the `tavily_search` tool.
            - Use the values in {preferences} to generate a list of search queries to find recent recipe URLs.
            - If the search results are poor or too few, refine and retry the tool.

        2. Call the `tavily_crawl` tool using the result URLs from `tavily_search`.

            ✅ Proceed to step 3 if **at least one** result has:
                - non-empty `raw_content`, and
                - a valid `page_url`.

            🔁 You may retry `tavily_crawl` **once** with refined queries if:
                - all `raw_content` fields are empty or irrelevant.

            ⚠️ Never call `tavily_crawl` more than **two times total**.

        3. Choose and modify a recipe using:
            - `recipe_contents` from `tavily_crawl`
            - `restrictions` and `preferences` from the user

            Choose the **first recipe** in the list that:
                - matches at least one value from {preferences}
                - and has valid `raw_content` and `page_url`

            Then, modify the recipe to:
                - substitute or remove ingredients based on {restrictions}
                - preserve relevance to user preferences

            Create a JSON object with these fields:
                - `original_page_url`: must match the `page_url` from tavily_crawl
                - `modified_recipe_content`: markdown-escaped text with only two sections:
                    - ## Ingredients  
                    - ## Directions  
                - `notes`: describe changes made to ingredients or method
                - `image_url`: a valid image URL from `image_urls` or `raw_content`
                - `recipe_title`: short 2–5 word name
                - `relevant_preferences`: only values from {preferences}, never from {restrictions} or anything new

        4. Call the `modify_recipe` tool with the above JSON object.

        5. Validate the modified recipe result:
            - ✅ Check that:
                - The recipe clearly reflects **at least one** of the user’s preferences
                - The ingredients and directions **do not violate any** restrictions
                - At least one ingredient has been substituted or removed due to a restriction  
                (**unless** the recipe was already compliant)
            - 🔁 If validation fails, repeat **step 3** with a different recipe from the same crawl results
            - ⛔ Do not repeat step 3 more than **twice total** (i.e., 3 total attempts including the first)
            - If still invalid after two retries, return the **most compliant available** result

        6. ✅ Return ONLY the validated output from the `modify_recipe` tool — no explanations, commentary, or extra text.

        ---

        ### ⚠️ Important Behavior Rules

        - Never call `tavily_crawl` until `tavily_search` returns valid URLs.
        - After first `tavily_crawl`, proceed to step 3 if at least one valid result is found.
        - Retry `tavily_crawl` only once if needed. Never more than twice total.
        - After calling `modify_recipe`, validate the result against:
            - Preference match
            - Restriction adherence
            - Ingredient modification (unless already compliant)
        - Retry step 3 with a different recipe if validation fails. Max two retries (three total attempts).
        - Always return exactly **one** modified recipe.

        ---

        ### ✅ Example valid input and output

        Input:
            - restrictions: ["vegan"]
            - preferences: ["italian", "asian", "chinese"]

        Output:
        [
        {{
            "original_page_url": "https://www.budgetbytes.com/creamy-tomato-spinach-pasta/",
            "modified_recipe_content": "## Ingredients\\n- ½ lb penne pasta\\n- 2 oz vegan cream cheese\\n\\n## Directions\\n1. Heat oil...\\n2. Add pasta...",
            "notes": "Replaced cream cheese with vegan cream cheese and butter with olive oil to accommodate a vegan restriction.",
            "image_url": "https://www.budgetbytes.com/wp-content/uploads/2020/05/CreamyTomatoSpinachPasta_FrontBiteOnFork.jpg",
            "recipe_title": "Creamy Tomato Spinach Pasta",
            "relevant_preferences": ["italian"]
        }}
        ]
        """

    prompt = PromptTemplate.from_template(prompt_template)
    prompt = prompt.format(
        restrictions=state["user_info"].restrictions,
        preferences=state["user_info"].preferences,
    )

    llm = ChatOpenAI(model=OPEN_AI_MODEL, temperature=0)
    llm_with_tools = llm.bind_tools([tavily_search, tavily_crawl, modify_recipe])

    agent = create_react_agent(
        model=llm_with_tools,
        tools=[tavily_search, tavily_crawl, modify_recipe],
        prompt=prompt,
        response_format=("result", ModifiedRecipeContent),
        state_schema=State,
    )

    result_state = agent.invoke(state)
    validated_result = ModifiedRecipeContent.model_validate(result_state["structured_response"])
    state["modified_recipe_content"] = validated_result
    print(f"🧠 Recipe Modifier Agent finished")
    return state


