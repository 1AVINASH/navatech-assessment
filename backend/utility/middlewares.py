from time import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

from utility.logger import app_logger

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time()

        # Log request
        body = await request.body()
        app_logger.info(f"Request: {request.method} {request.url.path} - Body: {body.decode('utf-8') or 'None'}")

        response: Response = await call_next(request)

        duration = round(time() - start_time, 3)

        app_logger.info(f"Response: {request.method} {request.url.path} - Status: {response.status_code} - Time: {duration}s")

        return response