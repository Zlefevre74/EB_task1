
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .users import Base

import sqlalchemy as sa
from uuid import UUID, uuid4
from .orders import _values
from enums.access import PermissionLevel

role_permissions = sa.Table(
    'role_permissions',
    Base.metadata,
    sa.Column('role_id',  sa.ForeignKey('roles.id'), primary_key=True),
    sa.Column('permission_id', sa.ForeignKey('permissions.id'), primary_key=True),
)

class RoleModel(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        sa.Index('ix_roles_created', sa.desc('created_at'), sa.desc('id')),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(sa.String())
    description: Mapped[str] = mapped_column(sa.String())
    priority: Mapped[int] = mapped_column(sa.Integer())

    permissions: Mapped[list['PermissionModel']] = relationship(
        secondary=role_permissions, back_populates='roles'
    )

class PermissionModel(Base):
    __tablename__ = 'permissions'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(sa.String())
    description: Mapped[str] = mapped_column(sa.String())
    level: Mapped[PermissionLevel] = mapped_column(sa.Enum(PermissionLevel, name="permission_level", values_callable=_values))
    roles: Mapped[list['RoleModel']] = relationship(
        secondary=role_permissions, back_populates='permissions'
    )