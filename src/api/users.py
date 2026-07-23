from fastapi import APIRouter
from starlette import status
from db import get_session
from repos.users import create_user
from schemas.users import User, UserAdd

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(payload: UserAdd) -> User:
    async with get_session() as session:
        user = await create_user(session, payload.username)
        return User.model_validate(user)