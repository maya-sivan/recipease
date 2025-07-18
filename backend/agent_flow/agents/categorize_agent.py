from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from agent_flow.custom_types.agent_types import State
from langchain_openai import ChatOpenAI
from shared.models import UserInfo
from langgraph.prebuilt import create_react_agent
from agent_flow.setup import OPEN_AI_MODEL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def categorize_agent(state: State) -> State:
    logger.info("🔍 Categorize Agent")

    @tool
    def categorize_tool(user_info: UserInfo) -> UserInfo:
        """
            Use this tool to extract and categorize a user's food-related preferences and restrictions from natural language input.

            - Input:
                - object with the following fields:
                    - `preferences`: a list of preferred cuisines, flavors, or ingredients (e.g. ["spicy", "Mexican"])
                    - `restrictions`: a list of dietary restrictions, allergies, or foods to avoid (e.g. ["peanut allergy", "gluten-free"])
            - Output:
                - validated input

            The output must be valid JSON with only those two fields and no extra text.
        """
        return user_info

    prompt_template = """
        Your task is to act as a food preference and restriction analyzer. You will receive user text describing their food likes, dislikes, dietary requirements, and allergies.

        Your goal is to extract this information and categorize it into two lists: preferences and restrictions. You must then format this information as a JSON object for use by the following tool:
        - `categorize_tool`: validates the user's preferences and restrictions and returns them.
            - Input:
                - object with the following fields:
                    - `preferences`: a list of preferred cuisines, flavors, dishes, or ingredients (e.g. ["spicy", "Mexican"])
                    - `restrictions`: a list of dietary restrictions, allergies, or foods to avoid (e.g. ["peanut allergy", "gluten-free"])
            - Output:
                - validated input

        **Instructions:**

        1. Read the user's input carefully: {user_input}.
        2. Identify all mentions of:
            * Liked dishes, cuisines, flavors, or combinations (Preferences).
            * Allergies, specific diets (like vegan, keto, gluten-free), or foods to avoid (Restrictions).
        3. When extracting preferences:
            * Combine connected food items that are clearly part of the same thought (e.g. "burrito with rice", "salad with feta").
            * Only separate preferences into different list items when they are clearly independent, such as when separated by "or", commas, or listed distinctly.
        4. Create a JSON object with exactly two keys:
            * "preferences": An array containing concise descriptions of the user's preferences.
            * "restrictions": An array containing concise descriptions of the user's restrictions.
        5. Ensure no preference item is also listed as a restriction.
        6. Restrictions are always aspects that affect the user's ability to eat or drink something — allergies, diets, or avoidances.
        7. **Your output must be *only* the JSON object.** No extra text or formatting.

        **Example:**

        User Input: "I love spicy Thai and Mexican food, especially burritos with rice. I'm allergic to peanuts and avoid gluten."

        Output:
        {{
            "preferences": ["spicy Thai", "Mexican", "burritos with rice"],
            "restrictions": ["peanut allergy", "gluten-free"]
        }}
        """

    llm = ChatOpenAI(model=OPEN_AI_MODEL, temperature=0, api_key=OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools([categorize_tool])

    prompt = PromptTemplate.from_template(prompt_template)
    prompt = prompt.format(user_input=state["query"])

    agent = create_react_agent(
        model=llm_with_tools,
        tools=[categorize_tool],
        prompt=prompt,
        response_format=("result", UserInfo),
        state_schema=State,
    )

    result_state = agent.invoke(state)
    user_info: UserInfo = result_state["structured_response"]
    state["user_info"] = user_info
    return state

