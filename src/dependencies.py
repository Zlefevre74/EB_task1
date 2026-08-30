from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from repos.users import UserRepo
from services.users import UserService


async def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepo:
    return UserRepo(session)

async def get_user_service(repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(repo)