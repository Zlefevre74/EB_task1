import enum

from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .users import Base
from enums.billing import BillingPeriod, SubscriptionType

def _values(e: type[enum.Enum]) -> list[str]:
    return [m.value for m in e]

class OrderModel(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        sa.Index(
            'ix_orders_user_created', 'user_id', sa.desc('created_at'), sa.desc('id')),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(sa.ForeignKey('users.id'),
                                          nullable=False
    )
    subscription_type: Mapped[SubscriptionType] = mapped_column(
        sa.Enum(SubscriptionType, name='subscription_type', values_callable=_values),
        nullable=False,
    )
    billing_period: Mapped[BillingPeriod] = mapped_column(
        sa.Enum(BillingPeriod, name='billing_period', values_callable=_values),
        nullable=False,
    )
    license_expires_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False
    )
    discount: Mapped[Decimal] = mapped_column(sa.Numeric(5, 2), nullable=False)
    is_auto_renew: Mapped[bool] = mapped_column(
        sa.Boolean(), server_default=sa.true(), nullable=False
    )

    user: Mapped['UserModel'] = relationship(back_populates='orders')