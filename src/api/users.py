from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from starlette import status

from db import get_session
from mappers.users import to_dto, to_orm
from repos.users import UserRepo
from schemas.users import User, UserCreate, UserUpdate
from exceptions import NotFound


async def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepo:
    return UserRepo(session)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, repo: UserRepo = Depends(get_user_repo)) -> User:
    user = to_orm(payload)
    created = await repo.create(user)
    return to_dto(created)


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID, repo: UserRepo = Depends(get_user_repo)) -> User:
    user = await repo.get(user_id)
    if user is None:
        raise NotFound("User", user_id)
    return to_dto(user)


@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: UUID, payload: UserUpdate, repo: UserRepo = Depends(get_user_repo)) -> User:
    user = await repo.update(user_id, payload.model_dump(exclude_unset=True))
    if user is None:
        raise NotFound("User", user_id)
    return to_dto(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, repo: UserRepo = Depends(get_user_repo)) -> None:
    deleted = await repo.delete(user_id)
    if not deleted:
        raise NotFound("User", user_id)
