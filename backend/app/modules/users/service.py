from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from asyncio import to_thread

from app.modules.users.schemas import UserCreate
from app.modules.users.models import User
from app.core.security import get_password_hash

class EmailAlreadyRegisteredError(Exception):
    pass

async def register_user(session: AsyncSession, user_data: UserCreate) -> User:
    password_hash = await to_thread(get_password_hash, user_data.password.get_secret_value())

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