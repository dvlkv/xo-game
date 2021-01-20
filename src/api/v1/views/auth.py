from typing import Optional

from container import Services
from context import ViewWithContext
from aiohttp.web import json_response, Request
from modules import FieldError


class AuthView(ViewWithContext):
    async def post(self):
        req = await self.request.json()
        if not req['email']:
            raise FieldError('email', 'Email is empty')
        if not req['password']:
            raise FieldError('password', 'Password is empty')
        return json_response({"token": await Services.Auth().authorize_user(self.ctx(), req['email'], req['password'])})