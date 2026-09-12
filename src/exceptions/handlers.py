from starlette.responses import JSONResponse
from fastapi import Request, FastAPI
from exceptions.base import AppError
from schemas.errors import ErrorResponse

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=ErrorResponse(detail=str(exc)).model_dump())

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)

