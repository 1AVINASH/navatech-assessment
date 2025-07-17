import argparse

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from constants.defaults import DEFAULT_HOST, DEFAULT_PORT

# Utility
from utility.middlewares import LoggingMiddleware
from utility.logger import app_logger

# Infra
from infra.postgres.setup import db_cli
from infra.elasticsearch.setup import es_cli

## Managers
from services.organization.manager import org_manager
from services.admin.manager import admin_manager

## Routes
from services.organization.routes import organizations_router
from services.admin.routes import admins_router

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

@app.on_event("startup")
async def startup():
    # Initialize infra
    await db_cli.initialize()
    await es_cli.initialize()

    # Initialize Managers
    await org_manager.initialize()
    await admin_manager.initialize()

@app.on_event("shutdown")
async def shutdown():
    await db_cli.disconnect()
    await es_cli.close()

# Add routes
app.include_router(organizations_router, prefix="/api")
app.include_router(admins_router, prefix="/api")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Start the fast api server")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host to bind (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to bind (default: {DEFAULT_PORT})")
    args = parser.parse_args()
    uvicorn.run('app:app', host=args.host, port=args.port, log_level="info", reload=True)