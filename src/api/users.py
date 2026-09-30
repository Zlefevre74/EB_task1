from uuid import UUID
from fastapi import APIRouter, Depends
from starlette import status
from typing import Annotated

from services.users import UserService
from schemas.users import User, UserCreate, UserUpdate
from dependencies.users import get_read_user_service, get_user_service
from schemas.orders import Order, OrderCreate, OrderUpdate
from schemas.pagination import PaginationParams, Page

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: Annotated[UserService, Depends(get_user_service)]) -> User:
    return await service.create(payload)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: UUID, service: Annotated[UserService, Depends(get_read_user_service)]) -> User:
    return await service.get(user_id)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: UUID, payload: UserUpdate, service: Annotated[UserService, Depends(get_user_service)]) -> User:
    return await service.update(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, service: Annotated[UserService, Depends(get_user_service)]) -> None:
    return await service.delete(user_id)


@router.post("/{user_id}/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
        user_id: UUID,payload: OrderCreate,service: Annotated[UserService, Depends(get_user_service)],) -> Order:
    return await service.add_order(user_id, payload)


@router.get("/{user_id}/orders", response_model=Page[Order])
async def list_orders(user_id: UUID,params: Annotated[PaginationParams, Depends()],service: Annotated[UserService, Depends(get_read_user_service)],
) -> Page[Order]:
    return await service.list_orders(user_id, params)


@router.patch("/{user_id}/orders/{order_id}", response_model=Order)
async def update_order(user_id: UUID,order_id: UUID,payload: OrderUpdate,service: Annotated[UserService, Depends(get_user_service)],
) -> Order:
    return await service.update_order(user_id, order_id, payload)