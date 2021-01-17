from aiohttp.web import Application
from .views.account import AccountView
from .views.game import GameView
from .views.auth import AuthView


def setup_v1_routes(app: Application):
    router = app.router
    router.add_view('/account', AccountView)
    router.add_view('/game', GameView)
    router.add_view('/auth', AuthView)