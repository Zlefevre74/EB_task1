from models.accounts import AccountModel, BillingProfileModel
from schemas.accounts import (Account, AccountCreate, AccountUpdate, BillingProfile, BillingProfileCreate)
from schemas.pagination import PaginationParams, Page

def profile_to_orm(dto: BillingProfileCreate) -> BillingProfileModel:
    return BillingProfileModel(
        billing_email=dto.billing_email,
        payment_method=dto.payment_method,
        currency=dto.currency,
        )

def profile_to_dto(profile: BillingProfileModel) -> BillingProfile:
    return BillingProfile(
        id=profile.id,
        billing_email=profile.billing_email,
        payment_method=profile.payment_method,
        currency=profile.currency,
    )
def to_orm(dto: AccountCreate) -> AccountModel:
    account = AccountModel(
        title=dto.title,
        account_number=dto.account_number,
        opened_on=dto.opened_on,
    )
    if dto.billing_profile is not None:
        account.billing_profile = profile_to_orm(dto.billing_profile)
    return account


def to_dto(model: AccountModel) -> Account:
    return Account(
        id=model.id,
        title=model.title,
        account_number=model.account_number,
        created_at=model.created_at,
        opened_on=model.opened_on,
        billing_profile=(profile_to_dto(model.billing_profile) if
        model.billing_profile else None
        ),
    )

def to_page(rows: list[AccountModel], params: PaginationParams) -> Page[Account]:
    return Page[Account](
        items=[to_dto(a) for a in rows[:params.size]],
        size=params.size,
        has_next=len(rows) > params.size,
    )


def apply_update(model: AccountModel, dto: AccountUpdate) -> AccountModel:
    for field, value in dto.model_dump(exclude_unset=True, exclude={'billing_profile'}).items():
        setattr(model, field, value)
    return model