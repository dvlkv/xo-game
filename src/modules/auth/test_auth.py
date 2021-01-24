from sqlalchemy.ext.asyncio import AsyncSession
from container import setup_container, Container
from context import Context
from db.entities.user import User
from modules import UnauthorizedAccessError
import pytest
from utils import sha256


@pytest.fixture(scope='module')
def seed_test_data():
    async def f(session):
        async with session.begin():
            user = User(
                id=2,
                email="string@string.com",
                name="User",
                password=sha256("password" + "salt"),
                password_salt="salt"
            )
            session.add(user)
            await session.flush()
    return f


@pytest.mark.asyncio
async def test_authenticate(container: Container, session: AsyncSession):
    token = await container.Auth().authenticate_user(
        Context(session, False, None),
        "string@string.com",
        "password"
    )

    assert token == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZW1haWwiOiJzdHJpbmdAc3RyaW5nLmNvbSIsIm5hbWUiOiJVc2VyIn0" +\
        ".Mh2PDH7er-4EQf5_T2Fa9D2QiUvqjpdgLlGi6q97eWg"

@pytest.mark.asyncio
async def test_authenticate_fails(container: Container, session: AsyncSession):
    """Invalid password"""
    with pytest.raises(UnauthorizedAccessError):
        await container.Auth().authenticate_user(
            Context(session, False, None),
            "string@string.com",
            "passwrd"
        )

    """Email not found"""
    with pytest.raises(UnauthorizedAccessError):
        await container.Auth().authenticate_user(
            Context(session, False, None),
            "string@strig.com",
            "password"
        )
