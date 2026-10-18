from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.billing import BillingPeriod, SubscriptionType

class OrderCreate(BaseModel):
    subscription_type: SubscriptionType
    billing_period: BillingPeriod
    is_auto_renew: bool

class OrderUpdate(BaseModel):
    is_auto_renew: bool

class Order(BaseModel):
    id: UUID
    subscription_type: SubscriptionType
    billing_period: BillingPeriod
    license_expires_at: datetime
    discount: Decimal
    is_auto_renew: bool
    created_at: datetime

    model_config =  ConfigDict(from_attributes=True)
