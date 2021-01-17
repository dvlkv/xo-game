from aiohttp.web import Application, run_app
from routes import setup_routes
from db import setup_db
from seed_db import seed_db
from api import create_api


async def init_app() -> Application:
    # Setup DB
    await setup_db()
    await seed_db()

    # Setup web server
    app = Application()
    setup_routes(app)
    app.add_subapp('/api/v1', create_api())

    return app


if __name__ == '__main__':
    run_app(init_app())
