import asyncio
import pytest
from container import setup_container
from db import setup_db, create_session
from seed_db import seed_db
from utils.db import drop_db
from utils.tests import create_test_db


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='module')
def container():
    return setup_container()

@pytest.fixture(scope='module')
def seed_test_data():
    async def f(session):
        pass
    return f


@pytest.fixture(scope='module', autouse=True)
async def database(seed_test_data):
    url = await create_test_db("postgresql+asyncpg://postgres:postgres@localhost")
    engine = await setup_db(url)
    await seed_db()

    session = create_session()
    await seed_test_data(session)
    await session.close()

    yield engine

    await engine.dispose()
    await drop_db(url, force=True)


@pytest.fixture
async def session():
    session = create_session()
    yield session
    await session.close()
