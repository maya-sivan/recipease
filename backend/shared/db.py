from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os
from shared.ssm import get_ssm_parameter

load_dotenv()

MONOGODB_URI = get_ssm_parameter("mongoUri")
mongo_client = MongoClient(MONOGODB_URI, tlsCAFile=certifi.where())
db = mongo_client["tavily_db"]

queries_collection = db["queries"]
recipes_collection = db["recipes"]
background_tasks_collection = db["background_tasks"]