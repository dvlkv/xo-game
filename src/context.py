from aiohttp.web import middleware, Request, View
from db import create_session
from typing import NamedTuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession


class Context(NamedTuple):
    session: AsyncSession
    authorized: bool
    uid: Optional[int]


@middleware
async def context_middleware(request: Request, handler):
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
    def ctx(self) -> Context:
        return self.request['ctx']