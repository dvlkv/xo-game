from aiohttp import web
from api.decorators import authorized
from context import ViewWithContext
from modules import Users, UserModel
import json


class AccountView(ViewWithContext):
    @authorized
    async def get(self):
        return (await Users.user_by_id(self.ctx(), self.ctx().uid)).to_json()

    async def post(self):
        inp = await self.request.json()
        user = await Users.create_user(self.ctx(), UserModel(**inp))
        return web.json_response(user.to_json())
