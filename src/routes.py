from views.index import IndexView
from aiohttp.web import Application


def setup_routes(app: Application):
    router = app.router
    router.add_view('/', IndexView)