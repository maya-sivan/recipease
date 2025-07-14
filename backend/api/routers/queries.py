from datetime import datetime, timezone
from ..helpers.utils import background_job, convert_str_to_object_id
from shared.models import BgJob, JobRequest, QueryResponse, UpdateResolvedStatus
from fastapi import APIRouter, Request, HTTPException, status, BackgroundTasks
from typing import List, Optional
from uuid import uuid4

query_router = APIRouter()

@query_router.get("/all", response_description="List all queries", response_model=List[QueryResponse])
def list_queries(request: Request, skip: int | None = None, limit: int | None = None):
    queries = list(request.app.database["queries"].find().sort("created_at", -1))
    if skip is not None:
        queries = queries[skip:]
    if limit is not None:
        queries = queries[:limit]
    return queries

@query_router.get("/{id}", response_description="Get a single query by id", response_model=QueryResponse)
def find_query(id: str, request: Request):
    obj_id = convert_str_to_object_id(id)
    if (query := request.app.database["queries"].find_one({"_id": obj_id})) is not None:
        return query
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Query with ID {id} not found")

@query_router.delete("/{id}", response_description="Delete a single query by id")
def delete_query_and_related_recipes(id: str, request: Request):
    obj_id = convert_str_to_object_id(id)

    if (request.app.database["queries"].delete_one({"_id": obj_id})) is None:
        raise HTTPException(status_code=404, detail=f"Query with ID {id} not found")
   
    # Delete all recipes associated with this query_id
    result = request.app.database["recipes"].delete_many({"query_id": id})  
    print(f"Deleted query {id} and {result.deleted_count} related recipes.")
    return {"query_id": id, "related_recipes_deleted_count": result.deleted_count}

@query_router.post("/bg-job")
def start_job(payload: JobRequest, background_tasks: BackgroundTasks, request: Request):
    job_id = str(uuid4())

    request.app.database["background_tasks"].insert_one({
        "job_id": job_id,
        "user_email": payload.user_email,
        "query": payload.query,
        "status": "pending",
        "created_at": datetime.now(timezone.utc),
        "is_resolved": False
    })
    print(f"Starting job {job_id} for user {payload.user_email} with query {payload.query}")
    background_tasks.add_task(background_job, job_id, payload.user_email, payload.query, request.app.database["background_tasks"])
    return {"job_id": job_id}

@query_router.get("/bg-job/{job_id}", response_description="Get a bg job by its ID", response_model=BgJob)
def get_job(job_id: str, request: Request):
    job = request.app.database["background_tasks"].find_one({"job_id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {job_id} not found")
    return job


@query_router.put("/bg-job/{job_id}/is-resolved", response_description="Update a bg job by its ID", response_model=BgJob)
def update_job_is_resolved(job_id: str, payload: UpdateResolvedStatus, request: Request):
   result = request.app.database["background_tasks"].find_one_and_update(
        {"job_id": job_id},
        {"$set": {"is_resolved": payload.is_user_resolved}},
        return_document=True
    )

   if not result:
        raise HTTPException(status_code=404, detail="Job not found")

   return result


@query_router.post("/bg-jobs/all", response_description="List all bg jobs", response_model=List[BgJob])
def list_bg_jobs(request: Request, skip: int = 0, limit: int = 5, payload: Optional[dict] = None):
    bg_jobs = list(request.app.database["background_tasks"].find(payload).skip(skip).limit(limit).sort("created_at", -1))
    return bg_jobs

@query_router.post("/bg-jobs/count", response_description="Get the count of bg jobs", response_model=int)
def get_bg_jobs_count(request: Request, payload: Optional[dict] = None):
    count = request.app.database["background_tasks"].count_documents(payload)
    return count