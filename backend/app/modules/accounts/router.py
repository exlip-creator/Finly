from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.session import get_session
from app.modules.accounts.schemas import AccountCreate, AccountRead
from app.modules.users.models import User
from app.modules.accounts.service import get_accounts, create_account
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