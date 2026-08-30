from uuid import UUID
from exceptions import NotFound
from mappers.users import to_orm, to_dto, to_update_fields
from schemas.users import User, UserCreate, UserUpdate
from repos.users import UserRepo

class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo


    async def create(self, payload: UserCreate) -> User:
        user = to_orm(payload)
        created = await self.repo.create(user)
        return to_dto(created)


    async def get(self, user_id: UUID) -> User:
        user = await self.repo.get(user_id)
        if user is None:
            raise NotFound("User", user_id)
        return to_dto(user)



    async def update(self, user_id: UUID, payload: UserUpdate) -> User:
        fields = to_update_fields(payload)
        if not fields:
            return await self.get(user_id)
        user = await self.repo.update(user_id, fields)
        if user is None:
            raise NotFound("User", user_id)
        return to_dto(user)


    async def delete(self, user_id: UUID) -> None:
        deleted = await self.repo.delete(user_id)
        if not deleted:
            raise NotFound("User", user_id)



