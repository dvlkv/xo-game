from aiohttp.web import middleware
from db import create_session
from typing import NamedTuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession


class Context(NamedTuple):
    session: AsyncSession
    authorized: bool
    uid: Optional[int]


@middleware
async def context_middleware(request, handler):
    session = create_session()
    request['ctx'] = Context(session, False, None)
    response = await handler(request)
    await session.close()
    return response


class ViewWithContext:
    def ctx(self) -> Context:
        return self.request['ctx']