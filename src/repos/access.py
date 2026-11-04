from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models import RoleModel, PermissionModel
from repos.base import BaseRepo
from schemas.pagination import PaginationParams


class RoleRepo(BaseRepo):
    async def get(self, role_id: UUID) -> RoleModel | None:
        stmt = (
            select(RoleModel)
            .where(RoleModel.id == role_id,
        RoleModel.is_deleted.is_(False))
            .options(selectinload(RoleModel.permissions))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_with_pagination(self, params: PaginationParams) -> list[RoleModel]:
        stmt = (
            select(RoleModel)
            .where(RoleModel.is_deleted.is_(False))
            .options(selectinload(RoleModel.permissions))
        )
        return await self.paginate(stmt, params)

    async def get_permissions(self, ids: list[UUID]) -> list[PermissionModel]:
        stmt = select(PermissionModel).where(
            PermissionModel.id.in_(ids),
            PermissionModel.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())