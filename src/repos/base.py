from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import Base
from schemas.pagination import PageResult, PaginationParams


class BaseRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def save[T: Base](self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def paginate[T](self, stmt: Select, params: PaginationParams) -> PageResult[T]:
        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        rows = await self.session.execute(stmt.limit(params.size).offset(params.offset))
        return PageResult(items=rows.scalars().all(), total=total or 0)