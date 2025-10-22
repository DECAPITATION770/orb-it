from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from .config import settings

DATABASE_URL = settings.DB_URL
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, future=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
)

class Base(DeclarativeBase):
    ...

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session