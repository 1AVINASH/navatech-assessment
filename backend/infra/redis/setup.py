import os
from typing import Optional

from dotenv import load_dotenv
import redis.asyncio as redis

from utility.logger import app_logger

load_dotenv()

class RedisService:
    _redis: Optional[redis.Redis] = None

    def __init__(self):
        self._host = os.getenv("REDIS_HOST", "localhost")
        self._port = int(os.getenv("REDIS_PORT", 6379))
        self._db: int = int(os.getenv("REDIS_DB", 0))

    async def initialize(self):
        app_logger.info(f"Connecting to Redis at url: {self._host}:{self._port}")
        if self._redis is None:
            self._redis = redis.Redis(
                host=self._host,
                port=self._port,
                db=self._db,
                decode_responses=False
            )
        app_logger.info(f"Connected to Redis at url: {self._host}:{self._port}")

    @property
    def redis(self) -> redis.Redis:
        return self._redis


# Singleton instance
redis_service = RedisService()
