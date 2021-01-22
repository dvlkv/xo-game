from db import User
from context import Context
from sqlalchemy import *
from dataclasses import dataclass
from typing import Optional
import uuid
import re
from utils import sha256
from ..errors import *

# ignore
email_regex = re.compile(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")


@dataclass
class UserModel:
    """
    Data class containing user input, validates data after init (see: __post_init__)
    """
    email: str
    name: str
    password: str

    def __post_init__(self):
        if not email_regex.match(self.email.strip()):
            raise FieldError('email', 'Email should be valid email address')
        if len(self.name.strip()) == 0:
            raise FieldError('name', 'Name cannot be empty')
        if len(self.password.strip()) < 6:
            raise FieldError('password', 'Password length should be greater or equal then 6')


class UserRepo:
    async def user_by_id(self, ctx: Context, id: int) -> Optional[User]:
        stmt = select(User).where(User.id == id)
        user = await ctx.session.execute(stmt)
        res = user.first()
        return res[0] if res else None

    async def user_by_email(self, ctx: Context, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        user = await ctx.session.execute(stmt)
        res = user.first()
        return res[0] if res else None

    async def create_user(self, ctx: Context, input: UserModel) -> User:
        salt = str(uuid.uuid4())
        existing = await self.user_by_email(ctx, input.email.strip())
        if existing:
            raise EntityAlreadyExistsError("User with same email already exists")
        user = User(
            email=input.email.strip(),
            name=input.name.strip(),
            password=sha256(input.password + salt),
            password_salt=salt,
        )
        ctx.session.add(user)
        await ctx.session.flush()
        return user
