from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from models.users import UserModel

class UserRepo:
    def __init__(self, session: AsyncSession): self.session = session

    async def create(self, user: UserModel) -> UserModel:
        self.session.add(user)
        await self.session.flush()
        return user

    async def get(self, user_id: UUID) -> UserModel | None:
        stmt = select(UserModel).where(
            UserModel.id == user_id,
            UserModel.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update(self, user_id: UUID, fields: dict) -> UserModel | None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id,
                   UserModel.is_deleted.is_(False))
            .values(**fields)
            .returning(UserModel)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete(self, user_id: UUID) -> bool:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id, UserModel.is_deleted.is_(False))
            .values(is_deleted=True)
            .returning(UserModel.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None

