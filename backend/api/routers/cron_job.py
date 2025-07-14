from datetime import datetime, timedelta, timezone
from agent_flow.agent_flow import MasterAgent
from dotenv import dotenv_values
from fastapi import APIRouter, Request, Header
from pymongo.collection import Collection

config = dotenv_values(".env")

cron_job_router = APIRouter()

@cron_job_router.post("/run")
async def process_recent_queries(request: Request, x_cron_secret: str = Header(None, alias="X-Cron-Secret")):
    """
    This function is used to re-run saved queries to generate new recipes for them.
    It runs every 24 hours.
    It will not re-run queries that were created after the most recent run.
    There is a separate EBS environment for this cron job to avoid multiple instances of the cron job running at the same time.
    """
    print("***Entered run-cron***")

    if(x_cron_secret != config["CRON_SECRET"]):
        return "Forbidden", 403
    
    queries_collection: Collection = request.app.database["queries"]

    time_threshold = datetime.now(timezone.utc) - timedelta(seconds=60*60*24)

    
    queries_created_before_most_recent_run = queries_collection.find({
        "created_at": {"$lt": time_threshold}, # Don't re-run newer queries that were created after the most recent run
    })
    for query in queries_created_before_most_recent_run:
        print(f"Cron job running query {query['_id']}")
        master = MasterAgent()
        master.run_scheduled_query(query_id=query["_id"])
    return "OK", 200
