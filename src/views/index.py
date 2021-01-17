from aiohttp import web
import json


class IndexView(web.View):
    async def get(self):
        return web.Response(
            text=json.dumps({"name": 'lol'}),
            content_type="application/json"
        )
