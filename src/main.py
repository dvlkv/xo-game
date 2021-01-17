from aiohttp.web import Application, run_app
from routes import setup_routes
from db import setup_db
from seed_db import seed_db
from context import context_middleware
from api import setup_api_routes
from aiohttp_swagger import setup_swagger


async def init_app() -> Application:
    # Setup DB
    await setup_db()
    await seed_db()

    # Setup web server
    app = Application(middlewares=[
        context_middleware
    ])
    setup_routes(app)
    setup_api_routes(app)
    setup_swagger(app, swagger_url="/api/help")

    return app


if __name__ == '__main__':
    run_app(init_app())
