from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.accounts.models import Account
from app.modules.accounts.schemas import AccountCreate

async def create_account(account_data: AccountCreate, user_id: int, session: AsyncSession) -> Account:
    account = Account(
        user_id=user_id,
        name=account_data.name,
        start_balance=account_data.start_balance,
    )

    session.add(account)
    await session.commit()

    return account

async def get_accounts(user_id: int, session: AsyncSession) -> list[Account]:
    query = select(Account).where(Account.user_id == user_id).order_by(Account.id)
    accounts = await session.execute(query)
    return list(accounts.scalars().all())
