from aiohttp import web
from context import ViewWithContext
import json


class GameView(ViewWithContext):
    async def get(self):
        return web.json_response({"name": 'lol'})
