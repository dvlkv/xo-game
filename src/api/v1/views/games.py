from aiohttp import web
from context import ViewWithContext


class GamesView(ViewWithContext):
    async def get(self):
        return web.json_response({"name": 'lol'})
