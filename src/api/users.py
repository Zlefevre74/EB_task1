from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from db import get_session
from repos.users import create_user, get_user, update_user, delete_user
from schemas.users import User, UserAdd

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(payload: UserAdd) -> User:
    async with get_session() as session:
        user = await create_user(session, payload.username)
        return User.model_validate(user)


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def read_user(user_id: UUID) -> User:
    async with get_session() as session:
        user = await get_user(session, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return User.model_validate(user)


@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def edit_user(user_id: UUID, payload: UserAdd) -> User:
    async with get_session() as session:
        user = await update_user(session, user_id, payload.username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return User.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: UUID) -> None:
    async with get_session() as session:
        deleted = await delete_user(session, user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")