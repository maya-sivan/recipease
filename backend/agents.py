from typing import get_type_hints
from agent_types import HouseFeatures, LLMResponse, State
from setup import tavily_client
import openai
import json
from util.normalize_weights import normalize_weights

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


def extract_user_weights(state: State) -> State:
    print("🧠 LLM #1: Extracting feature weights from query")

    house_features = [k for k in get_type_hints(HouseFeatures).keys() if k != "is_for_sale"]

    system_prompt = (
     "You are an assistant helping to analyze a user's housing preferences.\n\n"
      f"You are given a fixed list of house features:\n{house_features}\n\n"
      "Your task is to return a JSON object with two keys: `extra_features` and `feature_weights`.\n\n"

      "First, create `extra_features`: this is a dictionary containing any user preferences **not already represented** in the fixed house features. "
      "Each key should be the name of an extra feature, and the value should be the appropriate Python type string (e.g., 'bool', 'int', 'str', 'float'). "
      "If the user expresses no such extra preferences, return an empty dictionary.\n\n"

      "Second, create `feature_weights`: this is a dictionary assigning an importance weight (from 0.0 to 1.0) to **every feature** the user cares about. "
      "The keys in this dictionary must include all the fixed house features **and** any keys from `extra_features`. "
      "The collective sum of ALL weights (from both the fixed house features and the extra features) must sum to exactly 1.0. Features not mentioned by the user should have a weight of 0.0.\n\n"

      "Reminder: Every key in `extra_features` must also appear in `feature_weights`.\n\n"
      "Return only a single JSON object with two keys: `extra_features` and `feature_weights`."
   )

    user_query = state["query"]
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
        results: LLMResponse = json.loads(content)
    except Exception as e:
        print("⚠️ Failed to parse LLM output:", e)
        raise

    # Normalize weights in case the LLM returned weights that don't sum to 1.0
    normalized_weights = normalize_weights(results["feature_weights"])
   
   
    state["feature_weights"] = normalized_weights
    state["extra_features"] = results["extra_features"]
    return state
