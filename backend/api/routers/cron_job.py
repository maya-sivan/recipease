from datetime import datetime, timedelta, timezone
from ..helpers.utils import background_job
from fastapi import APIRouter, Request, Header, BackgroundTasks
from pymongo.collection import Collection
from uuid import uuid4
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cron_job_router = APIRouter()

@cron_job_router.post("/run")
async def process_recent_queries(background_tasks: BackgroundTasks, request: Request):
    """
    This function is used to re-run saved queries to generate new recipes for them.
    It runs every 24 hours.
    It will not re-run queries that were created after the most recent run.
    There is a separate EBS environment for this cron job to avoid multiple instances of the cron job running at the same time.
    """
    logger.info("***Entered run-cron***")
    
    queries_collection: Collection = request.app.database["queries"]

    time_threshold = datetime.now(timezone.utc) - timedelta(seconds=60*60*24)

    
    queries_created_before_most_recent_run = queries_collection.find({
        "created_at": {"$lt": time_threshold}, # Don't re-run newer queries that were created after the most recent run
    })
    for query in queries_created_before_most_recent_run:
        logger.info(f"Cron job running query {query['_id']}")
        job_id = str(uuid4())
        request.app.database["background_tasks"].insert_one({
        "job_id": job_id,
        "user_email": query["user_email"],
        "query": query["query"],
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
        "is_resolved": False
        })
        logger.info(f"Starting job {job_id} for user {query["user_email"]} with query {query["query"]}")
        background_tasks.add_task(background_job, job_id=job_id, user_email=query["user_email"], query=query["query"], collection=request.app.database["background_tasks"], query_id=query["_id"])
    return "OK", 200
