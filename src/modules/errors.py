from dataclasses import dataclass


@dataclass
class FieldError(Exception):
    field: str
    text: str


class UnauthorizedAccessError(Exception):
    pass


@dataclass
class EntityAlreadyExists(Exception):
    text: str
    pass
