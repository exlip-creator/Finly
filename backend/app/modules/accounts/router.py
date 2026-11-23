from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.session import get_session
from app.modules.accounts.schemas import AccountCreate, AccountRead, AccountUpdate
from app.modules.users.models import User
from app.modules.accounts.service import get_accounts, create_account, get_account_by_id, update_account, NoSuchAccount, delete_account
from app.modules.users.dependencies import get_current_user

accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])

@accounts_router.get("", response_model=list[AccountRead])
async def read_accounts(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> list[AccountRead]:
    accounts = await get_accounts(current_user.id, session)
    return list(AccountRead.model_validate(acc) for acc in accounts)

@accounts_router.post("", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def add_account(
        account_data: AccountCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> AccountRead:
    new_account = await create_account(account_data, current_user.id, session)
    return AccountRead.model_validate(new_account)

@accounts_router.get("/{account_id}", response_model=AccountRead)
async def read_account_by_id(
        account_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> AccountRead:
    account = await get_account_by_id(account_id, current_user.id, session)

    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    return AccountRead.model_validate(account)


@accounts_router.patch("/{account_id}", response_model=AccountRead)
async def update_account_by_id(
        update_data: AccountUpdate,
        account_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> AccountRead:
    try:
        updated_account = await update_account(update_data, account_id, current_user.id, session)
        return AccountRead.model_validate(updated_account)
    except NoSuchAccount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")


@accounts_router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account_by_id(
        account_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> None:
    try:
        await delete_account(account_id, current_user.id, session)
        return None
    except NoSuchAccount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")