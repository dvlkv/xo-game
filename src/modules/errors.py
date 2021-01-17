class FieldError(Exception):
    field: str
    text: str


class UnauthorizedAccessError(Exception):
    pass
