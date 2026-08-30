from uuid import UUID
from fastapi import APIRouter, Depends
from starlette import status

from services.users import UserService
from schemas.users import User, UserCreate, UserUpdate
from dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)) -> User:
    return await service.create(payload)


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID, service: UserService = Depends(get_user_service)) -> User:
    return await service.get(user_id)


@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: UUID, payload: UserUpdate, service: UserService = Depends(get_user_service)) -> User:
    return await service.update(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)) -> None:
    return await service.delete(user_id)
