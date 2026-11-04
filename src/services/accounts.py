from uuid import UUID

from exceptions import NotFound
from mappers.accounts import to_orm, to_dto, to_page, profile_to_orm, apply_update
from models import AccountModel
from repos.accounts import AccountRepo
from schemas.accounts import AccountCreate, Account, AccountUpdate
from schemas.pagination import PaginationParams, Page


class AccountService:
    def __init__(self, repo: AccountRepo) -> None:
        self.repo = repo

    async def _get_or_raise(self, account_id: UUID) -> AccountModel:
        account = await self.repo.get(account_id)
        if account is None:
            raise NotFound(f'Account with id {account_id} was not found.')
        return account

    async def list_accounts(self, params: PaginationParams) -> Page[Account]:
        return to_page(await self.repo.get_with_pagination(params), params)

    async def create(self, payload: AccountCreate) -> Account:
        saved = await self.repo.save(to_orm(payload))
        return to_dto(await self._get_or_raise(saved.id))

    async def get(self, account_id: UUID) -> Account:
        return to_dto(await self._get_or_raise(account_id))

    async def update(self, account_id: UUID, payload: AccountUpdate)-> Account:
        account = await self._get_or_raise(account_id)
        apply_update(account, payload)
        if payload.billing_profile is not None:
            if account.billing_profile is not None:
                account.billing_profile.is_deleted = True
            account.billing_profile = profile_to_orm(payload.billing_profile)
        await self.repo.save(account)
        return to_dto(await self._get_or_raise(account_id))

async def delete(self, account_id: UUID) -> None:
        account = await self._get_or_raise(account_id)
        account.is_deleted = True
        if account.billing_profile is not None:
            account.billing_profile.is_deleted = True
        await self.repo.save(account)

