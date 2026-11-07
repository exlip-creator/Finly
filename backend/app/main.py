from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import  SQLAlchemyError
from sqlalchemy import text

from app.db.session import get_session
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

@app.get("/health/db", tags=["health"])
async def db_health_check(session: AsyncSession = Depends(get_session)) -> dict:
    try:
        result = await session.execute(text("SELECT 1;"))
        return {"status": "ok", "database": result.scalar_one()}
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        ) from error