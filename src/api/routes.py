from aiohttp.web import Application
from .v1.routes import setup_v1_routes


def setup_api_routes(app: Application):
    setup_v1_routes(app)