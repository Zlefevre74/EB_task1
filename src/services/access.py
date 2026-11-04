from uuid import UUID

from exceptions import NotFound
from mappers.access import to_orm, to_dto, to_page, apply_update, permission_to_orm
from models import RoleModel
from repos.access import RoleRepo
from schemas.access import RoleCreate, Role, RoleUpdate, PermissionCreate, PermissionLink
from schemas.pagination import PaginationParams, Page


class RoleService:
    def __init__(self, repo: RoleRepo) -> None:
        self.repo = repo

    async def _get_or_raise(self, role_id: UUID) -> RoleModel:
        role = await self.repo.get(role_id)
        if role is None:
            raise NotFound(f'Role with id {role_id} is not found')
        return role

    async def create(self, payload: RoleCreate) -> Role:
        saved = await self.repo.save(to_orm(payload))
        return to_dto(await self._get_or_raise(saved.id))

    async def get(self, role_id: UUID) -> Role:
        return to_dto(await self._get_or_raise(role_id))

    async def list_roles(self, params: PaginationParams) -> Page[Role]:
        return to_page(await self.repo.get_with_pagination(params),params)

    async def update(self, role_id: UUID, payload: RoleUpdate) ->  Role:
        role = await self._get_or_raise(role_id)
        apply_update(role, payload)
        await self._apply_permissions(role, payload.permissions)
        await self.repo.save(role)
        return to_dto(await self._get_or_raise(role_id))

    async def delete(self, role_id: UUID) -> None:
        role = await self._get_or_raise(role_id)
        role.is_deleted = True
        await self.repo.save(role)

    async def _apply_permissions(
            self, role: RoleModel, items: list[PermissionCreate | PermissionLink]) -> None:
        link_ids = [i.id for i in items if isinstance(i, PermissionLink)]
        found = {p.id: p for p in await self.repo.get_permissions(link_ids)} if link_ids else {}
        for item in items:
            if isinstance(item, PermissionLink):
                permission = found.get(item.id)
                if permission is None:
                    raise NotFound(f'Permission with id {item.id} is not found')
                role.permissions.append(permission)
            else:
                role.permissions.append(permission_to_orm(item))