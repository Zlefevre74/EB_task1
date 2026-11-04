from sqlalchemy.exc import IntegrityError

from sqlalchemy import Select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.conflict import Conflict
from models.users import Base
from schemas.pagination import PaginationParams


class BaseRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def save[T: Base](self, entity: T) -> T:
        try:
            self.session.add(entity)
            await self.session.flush()
        except IntegrityError as exc:
            await self.session.rollback()
            raise Conflict(f'{type(entity).__name__} is not unique.') from exc
        return entity

    async def paginate[T](self, stmt: Select, params: PaginationParams) -> list[T]:
        model = stmt.column_descriptions[0]['entity']
        if params.last_created_at and params.last_id:
            stmt = stmt.where(
                tuple_(model.created_at, model.id)
                < tuple_(params.last_created_at, params.last_id)
            )
        stmt = stmt.order_by(model.created_at.desc(), model.id.desc()).limit(params.size + 1)
        return list((await self.session.execute(stmt)).scalars().all())