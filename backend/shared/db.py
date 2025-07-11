from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os

load_dotenv()

MONOGODB_URI = os.getenv("MONOGODB_URI")
mongo_client = MongoClient(MONOGODB_URI, tlsCAFile=certifi.where())
db = mongo_client["tavily_db"]

queries_collection = db["queries"]
recipes_collection = db["recipes"]

# query_object = Query(
#     query="I like unique burgers, Chinese food, and Italian food. I'm allergic to peanuts and need gluten-free recipes.", 
#     user_email="mayasivannj@gmail.com", 
#     user_info=UserInfo(preferences=["unique burgers", "Chinese food", "Italian food"], 
#     restrictions=["peanuts", "gluten-free"]), 
#     created_at=datetime.datetime.now())

# queries_collection.insert_one(query_object.model_dump())

# recipe_object = Recipe(
#         query_id= "687045ecddd80b94204d6ff1",
#         restrictions=["peanuts", "gluten-free"],
#         found_at=datetime.datetime.now(),
#         recipe_content=ModifiedRecipeContent(
#             original_page_url="https://www.allrecipes.com/recipe/280256/super-salsa-burgers",
#             modified_recipe_content="## Ingredients\n\n- 1 ½ pounds ground beef\n- ½ cup salsa (use a salsa without peanuts)\n- ¼ cup gluten-free bread crumbs (ensure gluten-free)\n\n## Directions\n\n1. Combine ground beef, salsa, and gluten-free bread crumbs in a bowl using your hands. Shape into 12 patties.\n2. Cook in a skillet over medium-high heat until an instant-read thermometer inserted into the centers registers 160 degrees F (71 degrees C), about 10 minutes.\n\n## Nutrition Facts (per serving)\n\n|  |  |\n| --- | --- |\n| 115 | Calories |\n| 7g | Fat |\n| 2g | Carbs |\n| 10g | Protein |\n\nNotes: Replaced salsa to ensure it does not contain peanuts; used gluten-free bread crumbs for gluten restriction. The core burger structure is maintained.\n\n![Cheeseburger burger with salsa and all the fixings](https://www.allrecipes.com/thmb/rxaBmaPcusRO0EANATGyuHJNZNg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/280256super-salsa-burgersFranceCevallos-c4a09ee55ac94b5b9000743d67abc41b.jpg)', 'image_url': 'https://www.allrecipes.com/thmb/rxaBmaPcusRO0EANATGyuHJNZNg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/280256super-salsa-burgersFranceCevallos-c4a09ee55ac94b5b9000743d67abc41b.jpg",
#             recipe_title='Super Salsa Burgers',
#             relevant_preferences=["uniqe burgers"],
#             image_url="https://www.allrecipes.com/thmb/rxaBmaPcusRO0EANATGyuHJNZNg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/280256super-salsa-burgersFranceCevallos-c4a09ee55ac94b5b9000743d67abc41b.jpg",
#             notes="Replaced salsa to ensure it does not contain peanuts; used gluten-free bread crumbs for gluten restriction. The core burger structure is maintained."
#         ),
#     )

# recipes_collection.insert_one(recipe_object.model_dump())