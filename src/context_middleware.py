from typing import Optional

from aiohttp.web_middlewares import middleware
from aiohttp.web_request import Request

from container import Services
from context import Context
from db import create_session


@middleware
async def context_middleware(request: Request, handler):
    """Creates execution context from request and saves it in request['ctx']"""

    session = create_session()

    # check jwt token
    async with session.begin():
        jwt: Optional[str] = request.headers.get('Authorization')
        uid: Optional[int] = None
        if jwt is not None and jwt.startswith('Bearer '):
            token = jwt.split(' ')[1]
            user = await Services.Auth().authorize_user(Context(session, False, None), token)
            if user:
                uid = user.id

        request['ctx'] = Context(session, uid is not None, uid)

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