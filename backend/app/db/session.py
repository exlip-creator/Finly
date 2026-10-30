from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.postgres_user,
    password=settings.postgres_password.get_secret_value(),
    host=settings.db_host,
    port=settings.db_port,
    database=settings.postgres_db,
)

engine = create_async_engine(database_url)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)