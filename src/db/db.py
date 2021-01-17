import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from db import Base

_engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost/XOGame", 
    echo=True,
)


async def setup_db():
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return _engine


def create_session() -> AsyncSession:
    return AsyncSession(_engine)
