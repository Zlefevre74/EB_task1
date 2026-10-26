from sqlalchemy import select
from uuid import UUID
from sqlalchemy.orm import selectinload

from models.users import UserModel
from repos.base import BaseRepo
from schemas.pagination import PaginationParams


class UserRepo(BaseRepo):
    async def get(self, user_id: UUID) -> UserModel | None:
        stmt = (select(UserModel).where(
            UserModel.id == user_id,
            UserModel.is_deleted.is_(False),
            )
            .options(selectinload(UserModel.orders))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    async def get_with_pagination(self, params: PaginationParams) -> list[UserModel]:
        stmt = select(UserModel).where(UserModel.is_deleted.is_(False)).options(selectinload(UserModel.orders))
        return await self.paginate(stmt, params)
