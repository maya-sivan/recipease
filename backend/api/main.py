import certifi
from agent_flow.agent_flow import MasterAgent
from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from .routers.recipes import recipe_router
from .routers.queries import query_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from pymongo.collection import Collection
from datetime import datetime, timedelta, timezone

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

run_frequency = 60 * 60 * 3 # 3 hours

@app.on_event("startup")
@repeat_every(seconds=run_frequency, raise_exceptions=True)
async def process_recent_queries():
    """
    This function is used to re-run saved queries to generate new recipes for them.
    It runs every 3 hours.
    It will not re-run queries that were created after the most recent run.
    """
    print("***CRON JOB RUNNING***")
    queries_collection: Collection = app.database["queries"]

    time_threshold = datetime.now(timezone.utc) - timedelta(seconds=run_frequency)

    
    queries_created_before_most_recent_run = queries_collection.find({
        "created_at": {"$lt": time_threshold}, # Don't re-run newer queries that were created after the most recent run
    })
    for query in queries_created_before_most_recent_run:
        # master = MasterAgent()
        # master.run_scheduled_query(query_id=query["_id"])
        print("placeholder for cron job")
        #TODO: uncomment to run cron job

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(recipe_router, tags=["recipes"], prefix="/recipe")
app.include_router(query_router, tags=["queries"], prefix="/query")
