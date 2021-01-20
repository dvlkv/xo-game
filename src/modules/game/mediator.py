from context import Context
from db.entities.game import Game
from .repo import GameRepo


class GameMediator:
    """Provides access checks before accessing repository"""
    repo = GameRepo()

    async def start_game(self, ctx: Context, width: int, height: int) -> Game:
        pass