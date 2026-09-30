from typing import Sequence
from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass

from schemas.pagination import PaginationParams


@dataclass(frozen=True, slots=True)
class PageResult[T]:
    items: Sequence[T]
    total: int

async def paginate[T](session: AsyncSession, stmt: Select, params: PaginationParams) -> PageResult[T]:
    total = await session.scalar(select(func.count()).select_from(stmt.subquery()))
    rows = await session.execute(stmt.limit(params.size).offset(params.offset))
    return PageResult(items=rows.scalars().all(), total=total or 0)