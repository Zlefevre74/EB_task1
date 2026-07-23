from sqlalchemy.ext.asyncio import AsyncSession

from models.users import UserModel

async def create_user(session: AsyncSession, username: str) -> UserModel:
    user = UserModel(username=username)
    session.add(user)
    await session.flush()
    return user