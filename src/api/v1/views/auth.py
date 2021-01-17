from context import ViewWithContext
from aiohttp.web import json_response
from modules import Auth


class AuthView(ViewWithContext):
    async def post(self):
        req = await self.request.json()
        return json_response({"token": await Auth.authorize_user(self.ctx(), req['email'], req['password'])})