from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD.get_secret_value(),
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.POSTGRES_DB,
)

engine = create_async_engine(database_url)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)