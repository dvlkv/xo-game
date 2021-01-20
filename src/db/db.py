from typing import Union, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.engine import url
from .base import Base

_engine: Optional[AsyncEngine] = None


async def setup_db(connection_string: Union[str, url.URL]):
    global _engine
    if _engine:
        return _engine

    _engine = create_async_engine(
        connection_string,
    )

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return _engine


async def close_db():
    if _engine:
        await _engine.dispose()


def create_session() -> AsyncSession:
    global _engine

    return AsyncSession(_engine)
