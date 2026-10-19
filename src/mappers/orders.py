import sqlalchemy as sa

from models.orders import OrderModel
from schemas.orders import Order, OrderCreate, OrderUpdate


def to_orm(
        dto: OrderCreate

) -> OrderModel:
    period = dto.billing_period
    return OrderModel(
        subscription_type=dto.subscription_type,
        billing_period=period,
        license_expires_at=sa.func.now() + sa.func.make_interval(0, period.months),
        discount=period.discount,
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
        created_at=model.created_at,
    )


def apply_update(model: OrderModel, dto: OrderUpdate) -> OrderModel:
    model.is_auto_renew = dto.is_auto_renew
    return model