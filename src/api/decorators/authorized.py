from modules import UnauthorizedAccessError


def authorized(func):
    async def wrapper(self, **kwargs):
        if not self.ctx().authorized:
            raise UnauthorizedAccessError()
        return await func(self, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__

    return wrapper
