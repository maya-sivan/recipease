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
background_tasks_collection = db["background_tasks"]