from models.users import UserModel
from schemas.pagination import PageResult, PaginationParams, Page
from schemas.users import User, UserUpdate, UserCreate
from mappers import orders as order_mapper

def to_orm(dto: UserCreate) -> UserModel:
    user = UserModel(username=dto.username, email=dto.email, birth_date=dto.birth_date)
    user.orders = [order_mapper.to_orm(o) for o in dto.orders]
    return user

def to_dto(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        email=model.email,
        birth_date=model.birth_date,
        is_locked=model.is_locked,
        orders=[order_mapper.to_dto(o) for o in model.orders]
    )

def to_page(result: PageResult[UserModel], params: PaginationParams) -> Page[User]:
    return Page[User](
        items=[to_dto(u) for u in result.items],
        size=params.size,
        has_next=result.has_next,
    )

def apply_update(model: UserModel, dto: UserUpdate) -> UserModel:
    for field, value in dto.model_dump(exclude_unset=True, exclude={'orders'}).items():
        setattr(model, field, value)
    return model