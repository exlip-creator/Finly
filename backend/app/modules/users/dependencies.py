from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.session import get_session
from app.modules.users.models import User
from app.core.security import decode_access_token

bearer_auth = HTTPBearer(auto_error=False)

async def get_current_user(
        session: AsyncSession = Depends(get_session),
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer_auth)
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication credentials missing",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        user_id = decode_access_token(credentials.credentials)
        user = await session.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers = {"WWW-Authenticate": "Bearer"}
            )

        return user

    except (InvalidTokenError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        ) from error