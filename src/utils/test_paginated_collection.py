from dataclasses import dataclass
from utils import PaginatedCollection
import json


@dataclass
class Entity:
    a: int
    b: str

    def to_json(self):
        return self.__dict__


def test_paginated_collection_create_empty():
    collection = PaginatedCollection([], 0, lambda x: x if x is not None else 0)

    assert json.dumps(collection.to_json()) == '{"items": [], "total": 0, "cursor": 0}'
    assert collection.cursor == 0
    assert collection.total == 0


def test_paginated_collection_create_with_simple_data():
    collection = PaginatedCollection([1, 2, 3], 4, lambda x: x if x is not None else 0)

    assert json.dumps(collection.to_json()) == '{"items": [1, 2, 3], "total": 4, "cursor": 3}'
    assert collection.cursor == 3
    assert collection.total == 4


def test_paginated_collection_create_with_complex_data():
    collection = PaginatedCollection([Entity(1, "test"), Entity(2, "test 2")], 4, lambda x: x.a if x is not None else 0)

    assert json.dumps(collection.to_json()) == '{"items": [{"a": 1, "b": "test"}, {"a": 2, "b": "test 2"}], "total": 4, "cursor": 2}'
    assert collection.cursor == 2
    assert collection.total == 4