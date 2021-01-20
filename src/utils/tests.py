"""
Module containing utilities for testing

Warning: use this module only for tests
"""
import random
import string
from utils.db import create_db


def random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


async def create_test_db(connection_string: str):
    db_name = "XOGame-test-{}".format(random_string())
    return await create_db(connection_string, db_name)
