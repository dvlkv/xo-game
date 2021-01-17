from .user import *
from .game import *
from .errors import *

# TODO: use dependency injection

Users: UserRepo = UserRepo()
Games: GameRepo = GameRepo()
