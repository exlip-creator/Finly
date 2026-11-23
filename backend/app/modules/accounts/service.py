from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.accounts.models import Account
from app.modules.accounts.schemas import AccountCreate, AccountUpdate

class NoSuchAccount(Exception):
    pass


async def create_account(account_data: AccountCreate, user_id: int, session: AsyncSession) -> Account:
    account = Account(
        user_id=user_id,
        name=account_data.name,
        start_balance=account_data.start_balance,
        currency=account_data.currency,
    )

    session.add(account)
    await session.commit()

    return account


async def get_accounts(include_archived: bool, user_id: int, session: AsyncSession) -> list[Account]:
    query = select(Account).where(Account.user_id == user_id).order_by(Account.id)

    if not include_archived:
        query = query.where(Account.is_archived.is_(False))

    accounts = await session.execute(query)
    return list(accounts.scalars().all())


async def get_account_by_id(account_id: int, user_id: int, session: AsyncSession) -> Account | None:
    query = select(Account).where(Account.id == account_id, Account.user_id == user_id)
    account = await session.execute(query)
    return account.scalar_one_or_none()


async def update_account(update_data: AccountUpdate, account_id: int, user_id: int, session: AsyncSession) -> Account:
    account = await get_account_by_id(account_id, user_id, session)

    if account is None:
        raise NoSuchAccount

    account.name = update_data.name
    await session.commit()

    return account


async def delete_account(account_id: int, user_id: int, session: AsyncSession) -> None:
    account = await get_account_by_id(account_id, user_id, session)

    if account is None:
        raise NoSuchAccount

    await session.delete(account)
    await session.commit()

    return None

async def archive_account(account_id: int, user_id: int, session: AsyncSession, is_archived: bool) -> Account:
    account = await get_account_by_id(account_id, user_id, session)

    if account is None:
        raise NoSuchAccount

    account.is_archived = is_archived
    await session.commit()

    return account