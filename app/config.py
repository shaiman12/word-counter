import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-12345")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/word_counter")
    RQ_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    RQ_QUEUES = ["default"]
