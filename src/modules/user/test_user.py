from sqlalchemy.ext.asyncio import AsyncSession
from container import Container
from context import Context
from db.entities.user import User
from modules import UserModel, EntityAlreadyExistsError
import pytest
from utils import sha256


@pytest.fixture(scope='module')
def seed_test_data():
    async def f(session):
        async with session.begin():
            user = User(
                email="string@string.com",
                name="User",
                password=sha256("password" + "salt"),
                password_salt="salt"
            )
            session.add(user)
            await session.flush()
    return f


@pytest.mark.asyncio
async def test_create_user(container: Container, session: AsyncSession):
    async with session.begin():
        user = await container.Users().create_user(
            Context(session, False, None),
            UserModel(
                name="User ",
                email=" string@string.ru",
                password=" password",
            )
        )

        assert user.password == sha256(" password" + user.password_salt)
        assert user.name == "User"
        assert user.email == "string@string.ru"

@pytest.mark.asyncio
async def test_authenticate_fails(container: Container, session: AsyncSession):
    """Entity already exists"""
    with pytest.raises(EntityAlreadyExistsError):
        async with session.begin():
            await container.Users().create_user(
                Context(session, False, None),
                UserModel(
                    name="User ",
                    email=" string@string.com",
                    password=" password",
                )
            )
