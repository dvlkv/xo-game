from db import create_session
from db import User


async def seed_db():
    async with create_session() as session:
        async with session.begin():
            user = User(
                id=1,
                email="bot@bot.com",
                name="Computer",
                password="",
                password_salt="computer"
            )
            await session.merge(user)
            await session.flush()
