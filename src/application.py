from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from api.healthcheck import router
from api.users import router as user_router

def get_app() -> FastAPI:
    app = FastAPI(
        docs_url='/docs',
        openapi_url='/openapi.json',
        default_response_class=JSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(router)
    app.include_router(user_router)

    return app
