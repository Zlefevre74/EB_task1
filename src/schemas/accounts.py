from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict

from enums.billing import PaymentMethod


class BillingProfileBase(BaseModel):
    billing_email: EmailStr
    payment_method: PaymentMethod
    currency: str

class BillingProfileCreate(BillingProfileBase):
    pass

class BillingProfile(BillingProfileBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class AccountBase(BaseModel):
    title: str
    account_number: str
    opened_on: date

class Account(AccountBase):
    id: UUID
    created_at: datetime
    billing_profile: BillingProfile | None = None
    model_config = ConfigDict(from_attributes=True)

class AccountCreate(AccountBase):
    billing_profile: BillingProfileCreate | None = None

class AccountUpdate(BaseModel):
    title: str | None = None
    account_number: str | None = None
    billing_profile: BillingProfileCreate | None = None
    opened_on: date | None = None
