from typing import Annotated, AsyncGenerator, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session, get_read_session
from repos.access import RoleRepo
from services.access import RoleService


def role_service_dependency(
        session_dependency: Callable[[], AsyncGenerator[AsyncSession, None]],
) -> Callable[[AsyncSession], RoleService]:
    def dependency(
            session: Annotated[AsyncSession, Depends(session_dependency)],
    ) -> RoleService:
        return RoleService(RoleRepo(session))
    return dependency

get_read_role_service = role_service_dependency(get_read_session)
get_role_service = role_service_dependency(get_session)