from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.modules.users.schemas import UserCreate, UserRead
from app.db.session import get_session
from app.modules.users.service import register_user, EmailAlreadyRegisteredError

user_router = APIRouter(prefix="/auth", tags=["authentication"])

@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead, tags=["authentication"])
async def registrate(user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> UserRead:
    try:
        user = await register_user(session, user_data)
        return UserRead.model_validate(user)
    except EmailAlreadyRegisteredError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        ) from error