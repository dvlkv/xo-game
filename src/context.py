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


@middleware
async def context_middleware(request: Request, handler):
    """Creates execution context from request and saves it in request['ctx']"""
    session = create_session()
    request['ctx'] = Context(session, False, None)

    # Run non-GET requests in transaction
    #
    # To mutate data in GET requests you need to begin transaction explicitly
    if request.method != 'GET':
        async with session.begin():
            response = await handler(request)
    else:
        response = await handler(request)

    await session.close()
    return response


class ViewWithContext(View):
    """Base class for views with context"""
    def ctx(self) -> Context:
        return self.request['ctx']