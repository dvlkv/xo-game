from aiohttp import web
from api.decorators import authorized
from container import Services
from context import ViewWithContext
from modules import FieldError


class GamesView(ViewWithContext):
    #TODO: add cursor & count to docs
    @authorized
    async def get(self):
        query = self.request.query
        cursor = int(query.get('from') or 0)
        count = int(query.get('count') or 10)

        res = await Services.Games().get_games(self.ctx(), self.ctx().uid, cursor, count)
        return web.json_response(res.to_json())

    @authorized
    async def post(self):
        data = await self.request.json()
        if not data.get('size'):
            raise FieldError('size', 'Size is not specified')
        game = await Services.Games().start_game(self.ctx(), data['size'])
        return web.json_response(game.to_json())

