from datetime import datetime, timezone
from agent_flow.agent_flow import MasterAgent
from shared.models import BgJobStatus
from bson import ObjectId
from fastapi import HTTPException, status
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_str_to_object_id(id: str) -> ObjectId:
    try:
        obj_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    return obj_id

def background_job(job_id: str, user_email: str, query: str, collection, query_id: str | None = None):
    logger.info(f"Running job for: {user_email} | Query: {query}")
    try:
        collection.update_one(
            {"job_id": job_id},
            {"$set": {
                "status": BgJobStatus.RUNNING,
                "started_at": datetime.now(timezone.utc)
            }}
        )

        master = MasterAgent()
        if query_id:
            result = master.run_scheduled_query(query_id=query_id)
        else:
            result = master.run_new_query(user_email=user_email, query=query)

        logger.info(f"Job completed: {result}, now saving to db")

        collection.update_one(
            {"job_id": job_id},
            {"$set": {
                "status": BgJobStatus.COMPLETED,
                "completed_at": datetime.now(timezone.utc)
            }}
        )
    except Exception as e:
        logger.error(f"Error running job: {e}")
        collection.update_one(
            {"job_id": job_id},
            {"$set": {
                "status": BgJobStatus.FAILED,
                "completed_at": datetime.now(timezone.utc)
            }}
        )


