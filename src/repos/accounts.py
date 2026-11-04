from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlalchemy import select
from models import AccountModel
from repos.base import BaseRepo
from schemas.pagination import PaginationParams


class AccountRepo(BaseRepo):
    async def get(self, account_id: UUID) -> AccountModel | None:
        stmt = (
            select(AccountModel)
            .where(AccountModel.id == account_id,
                   AccountModel.is_deleted.is_(False))
            .options(selectinload(AccountModel.billing_profile))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_with_pagination(self, params: PaginationParams) -> list[AccountModel]:
        stmt = (
            select(AccountModel)
            .where(AccountModel.is_deleted.is_(False))
            .options(selectinload(AccountModel.billing_profile))
        )
        return await self.paginate(stmt, params)