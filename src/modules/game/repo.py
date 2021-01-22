from datetime import datetime

from sqlalchemy.orm import joinedload, raiseload

from db import Game, GameMove
from context import Context
from .checker import check_winner
from ..errors import FieldError, InvalidOperationError
from utils import PaginatedCollection
from sqlalchemy import *


class GameRepo:
    async def get_games(self, ctx: Context, uid: int, cursor: int, count: int) -> PaginatedCollection[Game]:
        result = await ctx.session.execute(
            select(Game).where(Game.uid == uid and Game.id > cursor).order_by(Game.id).limit(count)
        )
        data: list[Game] = [e for e, in result.unique()]
        result = await ctx.session.execute(
            select(func.count(Game.id)).where(Game.uid == uid and Game.id > cursor)
        )

        return PaginatedCollection(data, result.one()[0], lambda x: x.id if x is not None else 0)

    async def get_game(self, ctx: Context, id: int, load_moves=False) -> Game:
        stmt = select(Game).where(Game.id == id)
        if load_moves:
            stmt = stmt.options(joinedload(Game.moves))
        else:
            stmt = stmt.options(raiseload(Game.moves))
        result = await ctx.session.execute(stmt)
        game, = result.first()
        return game

    async def create_game(self, ctx: Context, size: int) -> Game:
        if 3 > size or size > 12:
            raise FieldError('size', 'Size is invalid')
        """Create empty game"""
        game = Game(
            uid=ctx.uid,
            size=size,
            started_at=datetime.now(),
            ended=False,
            winner=0,
            field=[[0 for x in range(size)] for y in range(size)],
            next_seq=1
        )
        ctx.session.add(game)
        await ctx.session.flush()
        return game

    async def make_move(self, ctx: Context, uid: int, gid: int, seq: int, x: int, y: int) -> (Game, GameMove):
        game = await self.get_game(ctx, gid, load_moves=True)
        if game.next_seq != seq:
            raise FieldError('seq', 'Seq is invalid')
        if game[x, y] != 0:
            raise FieldError('x,y', 'Position is not empty')
        if game.ended:
            raise InvalidOperationError("Game is ended")

        game[x, y] = uid

        game.next_seq += 1

        move = GameMove(
            game_id=game.id,
            seq=seq,
            uid=uid,
            time=datetime.now(),
            x=x,
            y=y
        )
        game.moves.append(move)

        # persist field
        # (ORM is not saving it wtf)
        await ctx.session.execute(update(Game).where(Game.id == game.id).ordered_values((Game.field, game.field)))

        await ctx.session.flush()

        winner = check_winner(game)

        if winner is not None:
            game.ended = True
            game.winner = winner
            game.duration = round((datetime.now() - game.started_at).total_seconds())
            await ctx.session.flush()

        return game, move

