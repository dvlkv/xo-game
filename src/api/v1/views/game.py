from aiohttp import web

from api.decorators import authorized
from container import Services
from context import ViewWithContext
from modules import FieldError


class GameView(ViewWithContext):
    @authorized
    async def get(self):
        id = int(self.request.match_info['id'])
        game = await Services.Games().get_game(self.ctx(), self.ctx().uid, id)
        return web.json_response(game.to_json())

    @authorized
    async def post(self):
        id = int(self.request.match_info['id'])
        body = await self.request.json()
        if not body.get('seq'):
            raise FieldError('seq', 'Seq is not specified')
        if body.get('x') is None:
            raise FieldError('x', 'x is not specified')
        if body.get('y') is None:
            raise FieldError('y', 'y is not specified')
        game, move = await Services.Games().make_move(
            self.ctx(),
            self.ctx().uid,
            id,
            int(body['seq']),
            int(body['x']),
            int(body['y'])
        )
        return web.json_response(game.to_json())
