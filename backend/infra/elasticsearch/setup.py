import os
from dotenv import load_dotenv

from elasticsearch import AsyncElasticsearch
load_dotenv()

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")

from utility.logger import app_logger
# Global variable to hold the Elasticsearch client instance
# It will be initialized during the application startup event

import os
from dotenv import load_dotenv
from utility.logger import app_logger

load_dotenv()

class ElasticsearchClient:
    _instance = None
    _client: AsyncElasticsearch = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ElasticsearchClient, cls).__new__(cls)
        return cls._instance

    async def initialize(self):
        if self._client:
            return

        url = os.getenv("ELASTICSEARCH_URL")
        user = os.getenv("ELASTICSEARCH_USER")
        password = os.getenv("ELASTICSEARCH_PASSWORD")

        try:
            app_logger.info(f"Connecting to Elasticsearch at {url} with user {user}")
            self._client = AsyncElasticsearch(
                hosts=[url],
                basic_auth=(user, password),
                verify_certs=False,  # Use proper certs in production
                request_timeout=30
            )

            for i in range(5):
                if not await self._client.ping():
                    app_logger.error("Connection to Elasticsearch failed during ping test.")
                else:
                    app_logger.info("Connected to Elasticsearch successfully.")
                    break
            else:
                raise ConnectionError("Could not connect to Elasticsearch.")

        except Exception as e:
            app_logger.error(f"Failed to initialize Elasticsearch client: {e}")
            raise

    async def get_client(self) -> AsyncElasticsearch:
        if self._client is None:
            await self.initialize()
        return self._client

    async def close(self):
        if self._client:
            await self._client.close()
            app_logger.info("Elasticsearch client connection closed.")

es_cli = ElasticsearchClient()