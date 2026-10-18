from sqlalchemy import Select, tuple_
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
        model = stmt.column_descriptions[0]['entity']
        if params.last_created_at and params.last_id:
            stmt = stmt.where(
                tuple_(model.created_at, model.id)
                < tuple_(params.last_created_at, params.last_id)
            )
        stmt = stmt.order_by(model.created_at.desc(), model.id.desc()).limit(params.size + 1)
        rows = (await self.session.execute(stmt)).scalars().all()
        return PageResult(items=rows[:params.size], has_next=len(rows) > params.size)