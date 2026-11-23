from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.categories.schemas import CategoryCreate
from app.modules.categories.models import Category

class CategoryAlreadyExistException(Exception):
    pass

async def create_category(category_data: CategoryCreate, user_id: int, session: AsyncSession) -> Category:
    query = (
        insert(Category)
            .values(user_id=user_id, name=category_data.name, kind=category_data.kind)
            .on_conflict_do_nothing(index_elements=[Category.user_id, Category.name, Category.kind])
            .returning(Category)
    )


    result = await session.execute(query)
    new_category = result.scalar_one_or_none()

    if not new_category:
        await session.rollback()
        raise CategoryAlreadyExistException

    await session.commit()

    return new_category

async def get_categories(include_archived: bool, user_id: int, session: AsyncSession) -> list[Category]:
    query = select(Category).where(Category.user_id == user_id).order_by(Category.id)

    if not include_archived:
        query = query.where(Category.is_archived.is_(False))

    categories = await session.execute(query)

    return list(categories.scalars().all())