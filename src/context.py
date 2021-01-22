from aiohttp.web import middleware, Request, View
from typing import NamedTuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from db.db import create_session


class Context(NamedTuple):
    """An object containing execution context: DB session and auth state"""
    session: AsyncSession
    authorized: bool
    uid: Optional[int]


@asynccontextmanager
async def create_context(authorized: bool, uid: Optional[int]) -> Context:
    session = create_session()
    try:
        yield Context(session, authorized, uid)
    finally:
        await session.close()


class ViewWithContext(View):
    """Base class for views with context"""
    def ctx(self) -> Context:
        return self.request['ctx']