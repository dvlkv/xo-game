from db import create_session
from db import User
from sqlalchemy import *


async def seed_db() -> None:
    """Populates database with an initial data"""
    async with create_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.id == 1))
            if result.first():
                return

            user = User(
                email="bot@bot.com",
                name="Computer",
                password="",
                password_salt="computer"
            )
            session.add(user)
            await session.flush()
