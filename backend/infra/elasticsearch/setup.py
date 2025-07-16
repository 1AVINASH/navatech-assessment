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

async def initialize_es_client():
    """
    Initializes the global Elasticsearch client.

    Args:
        es_url (str): The URL for the Elasticsearch host.
        es_user (str): The username for Elasticsearch authentication.
        es_password (str): The password for Elasticsearch authentication.
    """
    global _es_client
    if _es_client: return
    try:
        app_logger.info(f"v2 Connecting to Elasticsearch at {ELASTICSEARCH_URL} with user {ELASTICSEARCH_USER} and password {ELASTICSEARCH_PASSWORD}")
        _es_client = AsyncElasticsearch(
            hosts=[ELASTICSEARCH_URL],
            basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
            verify_certs=False, # Only for development, use proper CA certs in production
            request_timeout=30
        )
        app_logger.info(f"v2 Client {_es_client}")
        # if _es_client.ping():
        #     print("v2 client successfully pinged!")
        #     return _es_client
        # Ping the Elasticsearch cluster to verify the connection
        for i in range (5):
            if not await _es_client.ping():
                app_logger.error("Connection to Elasticsearch failed during ping test.")
            else: 
                app_logger.info("Connected to Elasticsearch successfully.")
                break
            raise ConnectionError("Could not connect to Elasticsearch.")
        return _es_client
    except Exception as e:
        app_logger.error(f"Failed to initialize Elasticsearch client: {e}")
        # app_logger.fatal(f"Failed to initialize Elasticsearch client: {e}")
        # Re-raise the exception to prevent the application from starting
        raise

async def close_es_client():
    """
    Closes the Elasticsearch client connection.
    """
    global _es_client
    if _es_client:
        await _es_client.close()
        app_logger.info("Elasticsearch client connection closed.")

_es_client: AsyncElasticsearch = None

async def get_es_client() -> AsyncElasticsearch:
    if _es_client is None:
        await initialize_es_client()
    return _es_client