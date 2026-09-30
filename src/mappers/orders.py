from datetime import datetime
from decimal import Decimal
from uuid import UUID

from models.orders import OrderModel
from schemas.orders import Order, OrderCreate, OrderUpdate


def to_orm(
        dto: OrderCreate,
        user_id: UUID,
        expires_at: datetime,
        discount: Decimal,
) -> OrderModel:
    return OrderModel(
        user_id=user_id,
        subscription_type=dto.subscription_type,
        billing_period=dto.billing_period,
        license_expires_at=expires_at,
        discount=discount,
        is_auto_renew=dto.is_auto_renew,
    )


def to_dto(model: OrderModel) -> Order:
    return Order(
        id=model.id,
        subscription_type=model.subscription_type,
        billing_period=model.billing_period,
        license_expires_at=model.license_expires_at,
        discount=model.discount,
        is_auto_renew=model.is_auto_renew,
    )


def apply_update(model: OrderModel, dto: OrderUpdate) -> OrderModel:
    model.is_auto_renew = dto.is_auto_renew
    return model