from fastapi import APIRouter

from schemas.healthcheck import HealthCheckResponse

healthcheck_router = APIRouter()


@healthcheck_router.get('/healthcheck', response_model=HealthCheckResponse)
async def healthcheck() -> HealthCheckResponse:
    return HealthCheckResponse(status='ok')
