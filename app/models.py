from datetime import datetime
from pymongo import MongoClient
from app.config import Config
from enum import Enum

client = MongoClient(Config.MONGO_URI)
db = client.word_counter


class JobStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class JobResult:
    @staticmethod
    def create(url: str, job_id: str) -> dict:
        result = {
            "url": url,
            "rq_job_id": job_id,
            "status": JobStatus.PENDING.value,
            "word_count": None,
            "words": [],
            "error": None,
            "created_at": datetime.utcnow(),
        }
        db.jobs.insert_one(result)
        return result

    @staticmethod
    def update(job_id: str, word_count: int, words: list) -> None:
        db.jobs.update_one(
            {"rq_job_id": job_id},
            {
                "$set": {
                    "word_count": word_count,
                    "words": words,
                    "status": JobStatus.COMPLETED.value,
                    "completed_at": datetime.utcnow(),
                }
            },
        )

    @staticmethod
    def mark_failed(job_id: str, error: str) -> None:
        db.jobs.update_one(
            {"rq_job_id": job_id},
            {
                "$set": {
                    "status": JobStatus.FAILED.value,
                    "error": error,
                    "completed_at": datetime.utcnow(),
                }
            },
        )

    @staticmethod
    def get_all():
        return db.jobs.find().sort("created_at", -1)

    @staticmethod
    def get_by_id(job_id: str) -> dict:
        return db.jobs.find_one({"rq_job_id": job_id})
