from models import PermissionModel, RoleModel
from schemas.access import PermissionCreate, Permission, RoleCreate, RoleUpdate, Role
from schemas.pagination import PaginationParams, Page


def permission_to_orm(dto: PermissionCreate) -> PermissionModel:
    return PermissionModel(code=dto.code, description=dto.description, level=dto.level)

def permission_to_dto(permission: PermissionModel) -> Permission:
    return Permission(
        id=permission.id,
        code=permission.code,
        description=permission.description,
        level=permission.level,
    )

def to_orm(dto: RoleCreate) -> RoleModel:
    role = RoleModel(name=dto.name, description=dto.description, priority=dto.priority)
    role.permissions = [permission_to_orm(p) for p in dto.permissions]
    return role

def to_dto(model: RoleModel) -> Role:
    return Role(
        id=model.id,
        name=model.name,
        description=model.description,
        priority=model.priority,
        created_at=model.created_at,
        permissions=[permission_to_dto(p) for p in model.permissions],
    )

def to_page(rows: list[RoleModel], params: PaginationParams) -> Page[Role]:
    return Page[Role](
        items=[to_dto(r) for r in rows[:params.size]],
        size=params.size,
        has_next=len(rows) > params.size,
        )

def apply_update(model: RoleModel, dto: RoleUpdate) -> RoleModel:
    for field, value in dto.model_dump(exclude_unset=True, exclude={'permissions'}).items():
        setattr(model, field, value)
    return model