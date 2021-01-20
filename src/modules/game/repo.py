from dataclasses import dataclass

from db import Game, GameMove
from context import Context
from utils import PaginatedCollection
from sqlalchemy import *


class GameRepo:
    async def get_user_games(self, ctx: Context, cursor: int, count: int) -> PaginatedCollection[Game]:
        result = await ctx.session.execute(
            select(Game).where(Game.uid == ctx.uid and Game.id > cursor).limit(count)
        )
        data: list[Game] = [e for e, in result.all()]
        result = await ctx.session.execute(
            select(func.count(Game.id)).where(Game.uid == ctx.uid and Game.id > cursor)
        )

        return PaginatedCollection(data, result.one()[0], data[len(data) - 1].id)


    def get_game(self, ctx: Context, game_id: int) -> Game:
        pass

    def create_game(self, ctx: Context, field_width: int, field_height: int) -> Game:
        pass


class GameMovesRepo:
    def get_moves(self, context: Context, game_id: int, cursor: int, count: int) -> PaginatedCollection[GameMove]:
        pass

    def make_move(self, context: Context, game_id: int, seq: int, x: int, y: int, uid: int) -> GameMove:
        pass


