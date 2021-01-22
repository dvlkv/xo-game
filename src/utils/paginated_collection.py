from dataclasses import dataclass, astuple
from typing import TypeVar, Generic, Union, Callable

T = TypeVar('T')


class PaginatedCollection(Generic[T]):
    items: list[T]
    total: int
    cursor: Union[int, str]

    def __init__(self, items: list[T], total: int, get_cursor: Callable[[Union[T, None]], Union[int, str]]):
        self.items = items
        self.total = total
        if len(items) > 0:
            self.cursor = get_cursor(items[len(items) - 1])
        else:
            self.cursor = get_cursor(None)

    def to_json(self):
        return dict(self.__dict__, items=[x.to_json() if hasattr(x, 'to_json') else x for x in self.items])
