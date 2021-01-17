from aiohttp import web
from context import ViewWithContext
import json


class GameView(web.View, ViewWithContext):
    async def get(self):
        return web.Response(text=json.dumps({ "name": 'lol' }), content_type="application/json")