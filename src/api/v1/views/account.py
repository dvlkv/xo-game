from aiohttp import web

from container import Services
from context import ViewWithContext
from api.decorators import authorized
from modules import UserModel


class AccountView(ViewWithContext):
    @authorized
    async def get(self):
        return web.json_response((await Services.Users().user_by_id(self.ctx(), self.ctx().uid)).to_json())

    async def post(self):
        inp = await self.request.json()
        user = await Services.Users().create_user(self.ctx(), UserModel(**inp))
        return web.json_response(user.to_json())
