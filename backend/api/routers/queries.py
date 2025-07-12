from datetime import datetime, timezone
from ..helpers.utils import convert_str_to_object_id
from shared.models import BgJob, JobRequest, QueryResponse
from fastapi import APIRouter, Request, HTTPException, status, BackgroundTasks
from typing import List
from uuid import uuid4
import time

query_router = APIRouter()

@query_router.get("/all", response_description="List all queries", response_model=List[QueryResponse])
def list_queries(request: Request):
    queries = list(request.app.database["queries"].find(limit=3))
    return queries

@query_router.get("/{id}", response_description="Get a single query by id", response_model=QueryResponse)
def find_query(id: str, request: Request):
    obj_id = convert_str_to_object_id(id)
    if (query := request.app.database["queries"].find_one({"_id": obj_id})) is not None:
        return query
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Query with ID {id} not found")

def background_job(job_id: str, user_email: str, query: str, collection):
    print(f"Running job for: {user_email} | Query: {query}")

    collection.update_one(
        {"job_id": job_id},
        {"$set": {
            "status": "running",
            "started_at": datetime.now(timezone.utc)
        }}
    )

    # Simulate work
    time.sleep(10)

    collection.update_one(
        {"job_id": job_id},
        {"$set": {
            "status": "completed",
            "completed_at": datetime.now(timezone.utc)
        }}
    )


@query_router.post("/create-new-bg-job")
def start_job(payload: JobRequest, background_tasks: BackgroundTasks, request: Request):
    job_id = str(uuid4())

    request.app.database["background_tasks"].insert_one({
        "job_id": job_id,
        "user_email": payload.user_email,
        "query": payload.query,
        "status": "pending",
        "created_at": datetime.now(timezone.utc)
    })
    print(f"Starting job {job_id} for user {payload.user_email} with query {payload.query}")
    background_tasks.add_task(background_job, job_id, payload.user_email, payload.query, request.app.database["background_tasks"])
    return {"job_id": job_id}

@query_router.get("/bg-job-status/{job_id}", response_description="Get a bg job by its ID", response_model=BgJob)
def get_job_status(job_id: str, request: Request):
    job = request.app.database["background_tasks"].find_one({"job_id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {job_id} not found")
    return job
