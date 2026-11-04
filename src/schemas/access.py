from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from enums.access import PermissionLevel


class PermissionBase(BaseModel):
    code: str
    description: str
    level: PermissionLevel

class PermissionCreate(PermissionBase):
    pass

class PermissionLink(BaseModel):
    id: UUID

class Permission(PermissionBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class RoleBase(BaseModel):
    name: str
    description: str
    priority: int

class Role(RoleBase):
    id: UUID
    created_at: datetime
    permissions: List[Permission] = []
    model_config = ConfigDict(from_attributes=True)

class RoleCreate(RoleBase):
    permissions: List[PermissionCreate] = []

class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    priority: int | None = None
    permissions: List[PermissionCreate | PermissionLink] = []