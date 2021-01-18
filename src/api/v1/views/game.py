from aiohttp import web
from context import ViewWithContext


class GameView(ViewWithContext):
    async def get(self):
        print(self.request.match_info['id'])
        return web.json_response({"name": 'lol'})

    async def post(self):
        return web.json_response({"name": 'lol'})
