from fastapi import FastAPI

from api.healthcheck import healthcheck_router
from api.users import router as user_router

def register_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router)
    app.include_router(user_router)