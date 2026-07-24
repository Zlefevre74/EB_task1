from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from models.users import UserModel

async def create_user(session: AsyncSession, username: str) -> UserModel:
    user = UserModel(username=username)
    session.add(user)
    await session.flush()
    return user

async def get_user(session: AsyncSession, user_id: UUID) -> UserModel | None:
    stmt = select(UserModel).where(UserModel.id == user_id,
    UserModel.is_deleted.is_(False),
    )
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def update_user(session: AsyncSession, user_id: UUID, username: str) -> UserModel | None:
    user = await get_user(session, user_id)
    if user is None:
        return None
    user.username = username
    await session.flush()
    return user

async def delete_user(session: AsyncSession, user_id: UUID) -> bool:
    user = await get_user(session, user_id)
    if user is None:
        return False
    user.is_deleted = True
    await session.flush()
    return True