from models.users import UserModel
from schemas.users import User, UserCreate

def to_orm(dto: UserCreate) -> UserModel:
    return UserModel(
        username=dto.username,
        email=dto.email,
        birth_date=dto.birth_date
    )

def to_dto(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        email=model.email,
        birth_date=model.birth_date,
        is_locked=model.is_locked
    )
