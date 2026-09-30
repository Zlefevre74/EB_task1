from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from models.orders import OrderModel
from models.users import Base, UserModel
from repos.pagination import PageResult, paginate
from schemas.pagination import PaginationParams

class UserRepo:
    def __init__(self, session: AsyncSession): self.session = session

    async def save[T: Base](self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get(self, user_id: UUID) -> UserModel | None:
        stmt = select(UserModel).where(
            UserModel.id == user_id,
            UserModel.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_order(self, user_id: UUID, order_id: UUID) -> OrderModel | None:
        stmt = select(OrderModel).where(
            OrderModel.id == order_id,
            OrderModel.user_id == user_id,
            OrderModel.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_orders(self, user_id: UUID, params: PaginationParams) -> PageResult[OrderModel]:
        stmt = (
            select(OrderModel)
            .where(OrderModel.user_id == user_id, OrderModel.is_deleted.is_(False))
            .order_by(OrderModel.created_at.desc(), OrderModel.id)
        )
        return await paginate(self.session, stmt, params)


