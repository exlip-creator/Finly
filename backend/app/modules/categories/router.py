from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.modules.users.dependencies import get_current_user
from app.modules.users.models import User
from app.db.session import get_session
from app.modules.categories.schemas import CategoryCreate, CategoryRead
from app.modules.categories.service import get_categories, create_category, CategoryAlreadyExistException

categories_router = APIRouter(prefix="/categories", tags=["categories"])

@categories_router.get("", response_model=list[CategoryRead])
async def read_categories(
        include_archived: bool = False,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> list[CategoryRead]:
    categories = await get_categories(include_archived, current_user.id, session)
    return list(CategoryRead.model_validate(category) for category in categories)

@categories_router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def add_category(
        category_data: CategoryCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> CategoryRead:
    try:
        new_category = await create_category(category_data, current_user.id, session)
        return CategoryRead.model_validate(new_category)
    except CategoryAlreadyExistException as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists"
        ) from error