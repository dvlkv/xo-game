from context import ViewWithContext
from aiohttp.web import json_response
from modules import Auth, FieldError


class AuthView(ViewWithContext):
    async def post(self):
        req = await self.request.json()
        if not req['email']:
            raise FieldError('email', 'Email is empty')
        if not req['password']:
            raise FieldError('password', 'Password is empty')
        
        return json_response({"token": await Auth.authorize_user(self.ctx(), req['email'], req['password'])})