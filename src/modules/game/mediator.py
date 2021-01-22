from context import Context
from db.entities.game import Game, select
from db.entities.game_move import GameMove
from utils import PaginatedCollection
from .repo import GameRepo
import random
from ..errors import NotFoundError


def _find_empty_point(game: Game, size: int):
    empty_points = []
    for y in range(size):
        for x in range(size):
            if game[x, y] == 0:
                empty_points.append((x, y))

    return random.choice(empty_points)


class GameMediator:
    """Provides access checks before accessing repository"""
    repo = GameRepo()

    async def get_game(self, ctx: Context, uid: int, id: int) -> Game:
        game = await self.repo.get_game(ctx, id, True)
        if game.uid != uid:
            raise NotFoundError()

        return game

    async def start_game(self, ctx: Context, size: int) -> Game:
        game = await self.repo.create_game(ctx, size)

        # if first should be a robot
        if random.choice([True, False]):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            game, move = await self.repo.make_move(ctx, 1, game.id, game.next_seq, x, y)
            return game

        return game

    async def get_games(self, ctx: Context, uid: int, cursor: int, count: int) -> PaginatedCollection[Game]:
        return await self.repo.get_games(ctx, uid, cursor, count)

    async def make_move(self, ctx: Context, uid: int, gid: int, seq: int, x: int, y: int) -> (Game, GameMove):
        """Makes user move and then computer move, returns game and next move"""
        game = await self.repo.get_game(ctx, gid)
        if game.uid != uid:
            raise NotFoundError()

        game, move = await self.repo.make_move(ctx, uid, gid, seq, x, y)
        if game.ended:
            return game, move

        comp_x, comp_y = _find_empty_point(game, game.size)
        return await self.repo.make_move(ctx, 1, gid, seq+1, comp_x, comp_y)


