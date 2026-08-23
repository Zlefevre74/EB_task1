from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from starlette import status

from db import get_session
from mappers.users import to_dto, to_orm
from repos.users import create_user, get_user, update_user,delete_user
from schemas.users import User, UserCreate, UserUpdate
from exceptions import NotFound

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(payload: UserCreate, session: AsyncSession = Depends(get_session)) -> User:
    user = to_orm(payload)
    created = await create_user(session, user)
    return to_dto(created)


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def read_user(user_id: UUID, session: AsyncSession = Depends(get_session)) -> User:
    user = await get_user(session, user_id)
    if user is None:
        raise NotFound("User", user_id)
    return to_dto(user)


@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def edit_user(user_id: UUID, payload: UserUpdate, session: AsyncSession = Depends(get_session)) -> User:
    user = await update_user(session, user_id, payload.username)
    if user is None:
        raise NotFound("User", user_id)
    return to_dto(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: UUID, session: AsyncSession = Depends(get_session)) -> None:
    deleted = await delete_user(session, user_id)
    if not deleted:
        raise NotFound("User", user_id)
