from agent_flow.custom_types.agent_types import State
from langchain_openai import ChatOpenAI
from shared.models import UserInfo
from langchain_core.tools.simple import Tool
from langgraph.prebuilt import create_react_agent
from agent_flow.setup import OPEN_AI_MODEL

def categorize_agent(state: State) -> State:
    print("🔍 Categorize Agent")
    llm = ChatOpenAI(model=OPEN_AI_MODEL, temperature=0)
    structured = llm.with_structured_output(UserInfo)

    def call_llm(query: str) -> UserInfo:
        return structured.invoke(query)

    extract_user_prefs = Tool.from_function(
        func=call_llm,
        name="categorize_agent",
        description="""
            Use this tool to extract and categorize a user's food-related preferences and restrictions from natural language input.

            - Input: A free-form user query describing likes, dislikes, allergies, or dietary needs.
            - Output: A JSON object with exactly two keys:
            - "preferences": a list of preferred cuisines, flavors, or ingredients (e.g. ["spicy", "Mexican"])
            - "restrictions": a list of dietary restrictions, allergies, or foods to avoid (e.g. ["peanut allergy", "gluten-free"])

            The output must be valid JSON with only those two fields and no extra text.
        """,
    )

    prompt = """
        Your task is to act as a food preference and restriction analyzer. You will receive user text describing their food likes, dislikes, dietary requirements, and allergies.

        Your goal is to extract this information and categorize it into two lists: preferences and restrictions. You must then format this information as a JSON object for use by a tool.

        **Instructions:**

        1.  Read the user's input carefully.
        2.  Identify all mentions of:
            *   Liked foods, cuisines, flavors, or ingredients (Preferences).
            *   Allergies, specific diets (like vegan, keto, gluten-free), or ingredients/foods to avoid (Restrictions).
        3.  Create a JSON object with exactly two keys:
            *   `"preferences"`: An array containing keywords or short descriptions of the user's preferences.
            *   `"restrictions"`: An array containing keywords or short descriptions of the user's restrictions.
        4.  Ensure the array values are concise strings.
        5.  Ensure that the preferences array never contains any values from the restrictions array.
        6.  Note that restrictions are always aspects that affect the user's ability to eat or drink something. Example: "vegetarian" is a restriction, NOT a preference because it affects the user's ability to eat meat.
        7.  **Crucially, your output must be *only* the JSON object.** Do not include any other text, explanations, or formatting outside of the JSON structure.

        **Example:**

        User Input: "I love spicy Thai and Mexican food, but I'm allergic to peanuts and need gluten-free recipes."

        Required Output:
        ```json
        {
        "preferences": ["spicy Thai", "Mexican"],
        "restrictions": ["peanut allergy", "gluten-free"]
        }
        ```
        """

    agent = create_react_agent(
        model=llm,
        tools=[extract_user_prefs],
        prompt=prompt,
        response_format=("result", UserInfo),
        state_schema=State,
    )

    result_state = agent.invoke(state)
    user_info: UserInfo = result_state["structured_response"]
    state["user_info"] = user_info
    return state

