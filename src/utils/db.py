from typing import Optional, Union

import asyncpg
from sqlalchemy.engine.url import make_url, URL


async def create_db(connection_string:  Union[str, URL], db_name: Optional[str] = None):
    """Creates database and returns it's url"""

    url: URL = connection_string if connection_string is URL else make_url(connection_string)
    database = db_name or url.database

    connection: asyncpg.Connection = await asyncpg.connect(user=url.username, password=url.password, host=url.host, port=url.port)
    await connection.execute("CREATE DATABASE \"{}\"".format(database))
    await connection.close()

    return url.set(database=database)


async def drop_db(connection_string: Union[str, URL], db_name: Optional[str] = None, force=False):
    """Drops database"""
    url: URL = connection_string if connection_string is URL else make_url(connection_string)
    database = db_name or url.database

    connection: asyncpg.Connection = await asyncpg.connect(
        user=url.username,
        password=url.password,
        host=url.host,
        port=url.port
    )
    if force:
        await connection.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{}'".format(database))
    await connection.execute("DROP DATABASE \"{}\"".format(database))
    await connection.close()


async def db_exists(connection_string: Union[str, URL]) -> bool:
    """Checks if database exists"""
    url: URL = connection_string if connection_string is URL else make_url(connection_string)
    database = url.database

    connection: asyncpg.Connection = await asyncpg.connect(user=url.username, password=url.password, host=url.host, port=url.port)
    result = await connection.fetch("SELECT datname FROM pg_catalog.pg_database WHERE datname = $1", database)
    await connection.close()
    return len(result) == 1
