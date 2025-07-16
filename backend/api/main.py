import os
import certifi
from dotenv.main import logger
from fastapi import FastAPI
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .routers.recipes import recipe_router
from .routers.queries import query_router
from .routers.cron_job import cron_job_router
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()
logger.info("INSIDE API FILE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)
@app.on_event("startup")
def startup_db_client():
    logger.info("Launching Mongo...")
    app.mongodb_client = MongoClient(os.getenv("MONOGODB_URI"), server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)

    try:
        app.mongodb_client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise e
    app.database = app.mongodb_client[os.getenv("DB_NAME")]
    logger.info("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend is running"}, 200

app.include_router(recipe_router, tags=["recipes"], prefix="/api/recipe")
app.include_router(query_router, tags=["queries"], prefix="/api/query")
app.include_router(cron_job_router, tags=["cron_job"], prefix="/api/cron_job")
