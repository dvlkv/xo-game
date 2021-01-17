from aiohttp.web import Application
from .views.account import AccountView
from .views.game import GameView


def setup_v1_routes(app: Application):
    router = app.router
    router.add_view('/api/v1/account', AccountView)
    router.add_view('/api/v1/game', GameView)