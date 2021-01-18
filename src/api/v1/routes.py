from aiohttp.web import Application
from .views.account import AccountView
from .views.games import GamesView
from .views.auth import AuthView
from .views.game import GameView


def setup_v1_routes(app: Application):
    router = app.router
    router.add_view('/auth', AuthView)
    router.add_view('/account', AccountView)

    router.add_view('/games', GamesView)
    router.add_view('/games/{id}', GameView)