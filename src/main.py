from aiohttp.web import Application, run_app
from container import setup_container
from db.db import setup_db
from seed_db import seed_db
from api import create_api


async def init_app() -> Application:
    # Setup container
    container = setup_container()

    # Setup DB
    await setup_db(container.config.db.connection_string())
    await seed_db()

    # Setup web server
    app = Application()
    app.add_subapp('/api/v1', create_api())

    return app


if __name__ == '__main__':
    run_app(init_app())
