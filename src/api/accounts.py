from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from dependencies.accounts import get_account_service,get_read_account_service
from schemas.accounts import Account, AccountCreate, AccountUpdate
from schemas.pagination import Page, PaginationParams
from services.accounts import AccountService

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/", response_model=Account,
             status_code=status.HTTP_201_CREATED)
async def create_account(
        payload: AccountCreate,
        service: Annotated[AccountService, Depends(get_account_service)],
) -> Account:
    return await service.create(payload)


@router.get("/{account_id}", response_model=Account)
async def get_account(
        account_id: UUID,
        service: Annotated[AccountService,
        Depends(get_read_account_service)],
) -> Account:
    return await service.get(account_id)


@router.put("/{account_id}", response_model=Account)
async def update_account(
        account_id: UUID,
        payload: AccountUpdate,
        service: Annotated[AccountService, Depends(get_account_service)],
) -> Account:
    return await service.update(account_id, payload)


@router.delete("/{account_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
        account_id: UUID,
        service: Annotated[AccountService, Depends(get_account_service)],
) -> None:
    return await service.delete(account_id)

@router.get("/", response_model=Page[Account])
async def list_accounts(
      params: Annotated[PaginationParams, Depends()],
      service: Annotated[AccountService,
Depends(get_read_account_service)],
) -> Page[Account]:
      return await service.list_accounts(params)