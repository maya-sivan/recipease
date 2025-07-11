import certifi
from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from .routers.recipes import recipe_router
from .routers.queries import query_router

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["MONOGODB_URI"], tlsCAFile=certifi.where())
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(recipe_router, tags=["recipes"], prefix="/recipe")
app.include_router(query_router, tags=["queries"], prefix="/query")