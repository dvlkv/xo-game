from dataclasses import dataclass


@dataclass
class FieldError(Exception):
    field: str
    text: str


class UnauthorizedAccessError(Exception):
    pass


@dataclass
class EntityAlreadyExistsError(Exception):
    text: str


class NotFoundError(Exception):
    pass


@dataclass
class InvalidOperationError(Exception):
    text: str
