from db import Game, GameMove
from context import Context
from utils import PaginatedCollection

class GameRepo:
    def get_user_games(self, context: Context, cursor: int, count: int) -> PaginatedCollection[Game]:
        pass

    def get_game(self, context: Context, game_id: int) -> Game:
        pass

    def start_game(self, context: Context, field_width: int, field_height: int) -> Game:
        pass


class GameMovesRepo:
    def get_moves(self, context: Context, game_id: int, cursor: int, count: int) -> PaginatedCollection[GameMove]:
        pass

    def make_move(self, context: Context, game_id: int, seq: int, x: int, y: int, uid: int) -> GameMove:
        pass


