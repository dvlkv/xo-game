from container import Container
from context import Context
from db.entities.user import User
import pytest

from modules import FieldError
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

@pytest.fixture
def ctx(session):
    return Context(session, True, 2)

@pytest.mark.asyncio
async def test_create_game(container: Container, ctx: Context):
    async with ctx.session.begin():
        game = await container.Games().start_game(
            ctx,
            5,
            10
        )

        # check if field is correct
        assert game.width == 5
        assert game.height == 10

        # check if user should make first or second move
        assert game.next_seq == 1 or game.next_seq == 2

        # check if game is created by user
        assert game.uid == ctx.uid
        assert len(game.field) == game.width * game.height
        assert game.winned == False

@pytest.mark.asyncio
async def test_create_game_fail_if_field_invalid(container: Container, ctx: Context):
    async with pytest.raises(FieldError):
        async with ctx.session.begin():
            await container.Games().start_game(
                ctx,
                -5,
                10
            )
    async with pytest.raises(FieldError):
        async with ctx.session.begin():
            await container.Games().start_game(
                ctx,
                -5,
                -10
            )
    async with pytest.raises(FieldError):
        async with ctx.session.begin():
            await container.Games().start_game(
                ctx,
                2,
                3
            )
    async with pytest.raises(FieldError):
        async with ctx.session.begin():
            await container.Games().start_game(
                ctx,
                2,
                1
            )

