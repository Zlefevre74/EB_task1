from typing import Annotated, AsyncGenerator, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session, get_read_session
from repos.accounts import AccountRepo
from services.accounts import AccountService


def account_service_dependency(
        session_dependency: Callable[[], AsyncGenerator[AsyncSession, None]],
) -> Callable[[AsyncSession], AccountService]:
    def dependency(
            session: Annotated[AsyncSession, Depends(session_dependency)],
    ) -> AccountService:
        return AccountService(AccountRepo(session))
    return dependency

get_read_account_service = account_service_dependency(get_read_session)
get_account_service = account_service_dependency(get_session)