from typing import Dict

from fastapi import APIRouter

healthcheck_router = APIRouter()


@healthcheck_router.get('/healthcheck')
async def healthcheck() -> Dict[str, str]:
    return {'status': 'ok'}
