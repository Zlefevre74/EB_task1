from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from dependencies.access import get_role_service,get_read_role_service
from schemas.access import Role, RoleCreate, RoleUpdate
from schemas.pagination import Page, PaginationParams
from services.access import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/", response_model=Role,
             status_code=status.HTTP_201_CREATED)
async def create_role(
        payload: RoleCreate,
        service: Annotated[RoleService, Depends(get_role_service)],
) -> Role:
    return await service.create(payload)


@router.get("/{role_id}", response_model=Role)
async def get_role(
        role_id: UUID,
        service: Annotated[RoleService, Depends(get_read_role_service)],
) -> Role:
    return await service.get(role_id)


@router.put("/{role_id}", response_model=Role)
async def update_role(
        role_id: UUID,
        payload: RoleUpdate,
        service: Annotated[RoleService, Depends(get_role_service)],
) -> Role:
    return await service.update(role_id, payload)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
        role_id: UUID,
        service: Annotated[RoleService, Depends(get_role_service)],
) -> None:
    return await service.delete(role_id)


@router.get("/", response_model=Page[Role])
async def list_roles(
        params: Annotated[PaginationParams, Depends()],
        service: Annotated[RoleService, Depends(get_read_role_service)],
) -> Page[Role]:
    return await service.list_roles(params)