from uuid import UUID
from exceptions import NotFound
from mappers.users import to_orm, to_dto, apply_update
from schemas.users import User, UserCreate, UserUpdate
from repos.users import UserRepo

class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo


    async def create(self, payload: UserCreate) -> User:
        user = to_orm(payload)
        created = await self.repo.save(user)
        return to_dto(created)


    async def get(self, user_id: UUID) -> User:
        user = await self.repo.get(user_id)
        if user is None:
            raise NotFound(f'User with id {user_id} is not found')
        return to_dto(user)



    async def update(self, user_id: UUID, payload: UserUpdate) -> User:
        user = await self.repo.get(user_id)
        if user is None:
            raise NotFound(f'User with id {user_id} is not found')
        apply_update(user, payload)
        saved = await self.repo.save(user)
        return to_dto(saved)


    async def delete(self, user_id: UUID) -> None:
        deleted = await self.repo.delete(user_id)
        if not deleted:
            raise NotFound(f'User with id {user_id} is not found')



