import argparse

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from constants.defaults import DEFAULT_HOST, DEFAULT_PORT
from utility.middlewares import LoggingMiddleware
from utility.logger import app_logger
from services.organization.routes import organizations_router
from services.admin.routes import admins_router
from infra.postgres.setup import db
from infra.elasticsearch.setup import initialize_es_client, close_es_client

app = FastAPI(debug=True)

# Add Middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or "*" in dev. Not needed if no frontend is hosted. Only needed for browsers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(organizations_router, prefix="/api")
app.include_router(admins_router, prefix="/api")

@app.on_event("startup")
async def startup():
    await db.connect()
    await initialize_es_client()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    await close_es_client()


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Start the fast api server")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host to bind (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to bind (default: {DEFAULT_PORT})")
    args = parser.parse_args()
    uvicorn.run('app:app', host=args.host, port=args.port, log_level="info", reload=True)