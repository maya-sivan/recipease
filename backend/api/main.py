import certifi
from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from .routers.recipes import recipe_router
from .routers.queries import query_router
from .routers.cron_job import cron_job_router
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config['FRONTEND_URL']],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

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
app.include_router(cron_job_router, tags=["cron_job"], prefix="/cron_job")
