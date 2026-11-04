from fastapi import FastAPI

from api.healthcheck import healthcheck_router
from api.users import router as user_router
from api.accounts import router as account_router
from api.access import router as access_router

def register_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router)
    app.include_router(user_router)
    app.include_router(account_router)
    app.include_router(access_router)