from uuid import UUID

from exceptions import NotFound
from mappers.users import to_orm, to_dto, apply_update, to_page
from schemas.users import User, UserCreate, UserUpdate
from repos.users import UserRepo
from models.users import UserModel
from mappers import orders as order_mapper
from schemas.pagination import Page, PaginationParams
from schemas.orders import OrderCreate, OrderUpdate

class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    async def _get_or_raise(self, user_id: UUID) -> UserModel:
        user = await self.repo.get(user_id)
        if user is None:
            raise NotFound(f'User with id {user_id} is not found')
        return user

    async def create(self, payload: UserCreate) -> User:
        saved = await self.repo.save(to_orm(payload))
        return to_dto(await self._get_or_raise(saved.id))

    async def get(self, user_id: UUID) -> User:
        return to_dto(await self._get_or_raise(user_id))

    async def list_users(self, params: PaginationParams) -> Page[User]:
        return to_page(await self.repo.get_with_pagination(params), params)

    async def update(self, user_id: UUID, payload: UserUpdate) -> User:
        user = await self._get_or_raise(user_id)
        apply_update(user, payload)
        self._apply_orders(user, payload.orders)
        saved = await self.repo.save(user)
        return to_dto(await self._get_or_raise(user_id))


    async def delete(self, user_id: UUID) -> None:
        user = await self._get_or_raise(user_id)
        user.is_deleted = True
        for order in user.orders:
            order.is_deleted = True
        await self.repo.save(user)

    def _apply_orders(self, user: UserModel, items: list[OrderCreate | OrderUpdate]) -> None:
        existing = {o.id: o for o in user.orders}
        for item in items:
            if isinstance(item, OrderUpdate):
                order = existing.get(item.id)
                if order is None:
                    raise NotFound(f'Order with id {item.id} is not found')
                order_mapper.apply_update(order, item)
            else:
                user.orders.append(order_mapper.to_orm(item))





