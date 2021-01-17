from aiohttp.web import Application
from .routes import setup_v1_routes
from aiohttp_swagger import setup_swagger
from api.middlewares import error_middleware
from context import context_middleware

def create_api():
    app = Application(middlewares=[
        error_middleware,
        context_middleware
    ])
    setup_v1_routes(app)
    setup_swagger(
        app,
        swagger_url="/help",
        api_base_url="/api/v1",
        swagger_from_file="src/api/v1/doc.yaml"
    )
    return app