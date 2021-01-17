from dataclasses import dataclass, astuple
from typing import TypeVar, Generic, Union
T = TypeVar('T')


@dataclass
class PaginatedCollection(Generic[T]):
    items: list[T]
    total: int
    cursor: Union[int, str]

    def __iter__(self):
        yield from astuple(self)
