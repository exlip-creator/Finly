from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from asyncio import to_thread

from app.modules.users.schemas import UserCreate, UserLogin
from app.modules.users.models import User
from app.core.security import get_password_hash, verify_password

class EmailAlreadyRegisteredError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

async def register_user(session: AsyncSession, user_data: UserCreate) -> User:
    password = user_data.password.get_secret_value()
    password_hash = await to_thread(get_password_hash, password)

    query = (
        insert(User)
             .values(email=user_data.email, password_hash=password_hash)
             .on_conflict_do_nothing(index_elements=[User.email])
             .returning(User)
    )

    async with session.begin():
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise EmailAlreadyRegisteredError

    return user

async def login_user(session: AsyncSession, user_data: UserLogin) -> User:
    query = select(User).where(User.email == user_data.email)

    async with session.begin():
        result = await session.execute(query)
        user = result.scalar_one_or_none()

    if user is None:
        raise InvalidCredentialsError

    password = user_data.password.get_secret_value()
    password_is_valid = await to_thread(verify_password, password, user.password_hash)

    if not password_is_valid:
        raise InvalidCredentialsError

    return user