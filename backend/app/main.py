from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import  SQLAlchemyError
from sqlalchemy import text

from app.db.session import get_session
from app.core.config import settings
from app.modules.users.router import user_router

app = FastAPI(title=settings.APP_NAME)
app.include_router(user_router)

@app.exception_handler(RequestValidationError)
async def validation_error_handler(_request: Request, error: RequestValidationError) -> JSONResponse:
    details = [
        {
            "loc": item["loc"],
            "msg": item["msg"],
            "type": item["type"]
        }
        for item in error.errors()
    ]

    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": details})

@app.get("/health/db", tags=["health"])
async def db_health_check(session: AsyncSession = Depends(get_session)) -> dict:
    try:
        result = await session.execute(text("SELECT 1;"))
        return {"status": "ok", "database": result.scalar_one()}
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable"
        ) from error