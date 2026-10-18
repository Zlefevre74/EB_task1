from uuid import UUID

from exceptions import NotFound
from mappers.users import to_orm, to_dto, apply_update
from schemas.users import User, UserCreate, UserUpdate
from repos.users import UserRepo
from models.users import UserModel
from datetime import datetime, timezone

from mappers import orders as order_mapper
from schemas.pagination import Page, PaginationParams
from schemas.orders import Order, OrderCreate, OrderUpdate

class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    async def _get_or_raise(self, user_id: UUID) -> UserModel:
        user = await self.repo.get(user_id)
        if user is None:
            raise NotFound(f'User with id {user_id} is not found')
        return user

    async def create(self, payload: UserCreate) -> User:
        user = to_orm(payload)
        created = await self.repo.save(user)
        return to_dto(created)

    async def get(self, user_id: UUID) -> User:
        return to_dto(await self._get_or_raise(user_id))

    async def update(self, user_id: UUID, payload: UserUpdate) -> User:
        user = await self._get_or_raise(user_id)
        apply_update(user, payload)
        saved = await self.repo.save(user)
        return to_dto(saved)


    async def delete(self, user_id: UUID) -> None:
        user = await self._get_or_raise(user_id)
        user.is_deleted = True
        await self.repo.save(user)

    async def add_order(self, user_id: UUID, payload: OrderCreate) -> Order:
        user = await self._get_or_raise(user_id)
        period = payload.billing_period
        now = datetime.now(timezone.utc)
        order = order_mapper.to_orm(payload, user.id, period.expiry_from(now), period.discount)
        return order_mapper.to_dto(await self.repo.save(order))

    async def list_orders(self, user_id: UUID, params: PaginationParams) -> Page[Order]:
        await self._get_or_raise(user_id)
        result = await self.repo.list_orders(user_id, params)
        return Page[Order](
            items=[order_mapper.to_dto(o) for o in result.items],
            size=params.size,
            has_next=result.has_next,
        )

    async def update_order(self, user_id: UUID, order_id: UUID, payload: OrderUpdate) -> Order:
        order = await self.repo.get_order(user_id, order_id)
        if order is None:
            raise NotFound(f'Order with id {order_id} is not found')
        order_mapper.apply_update(order, payload)
        return order_mapper.to_dto(await self.repo.save(order))



