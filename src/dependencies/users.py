from typing import Annotated, Callable, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session, get_read_session
from repos.users import UserRepo
from services.users import UserService


def user_service_dependency(
        session_dependency: Callable[[], AsyncGenerator[AsyncSession, None]]
) -> Callable[[AsyncSession], UserService]:
    def dependency(
            session: Annotated[AsyncSession, Depends(session_dependency)],
    ) -> UserService:
        return UserService(UserRepo(session))
    return dependency

get_read_user_service = user_service_dependency(get_read_session)
get_user_service = user_service_dependency(get_session)