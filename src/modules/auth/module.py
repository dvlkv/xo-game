from context import Context
from db.entities.user import User
from modules import UnauthorizedAccessError, UserModule
from utils import sha256
from typing import NamedTuple, Optional
import jwt


class JWTInfo(NamedTuple):
    id: int
    email: str
    name: str


class AuthModule:
    """Contains tools for JWT token management"""

    def __init__(self, users: UserModule, secret: str):
        self.users = users
        self.secret = secret

    async def authenticate_user(self, ctx: Context, email: str, password: str) -> str:
        """Authenticates user and returns JWT token containing user info"""
        user = await self.users.user_by_email(ctx, email)

        if not user:
            raise UnauthorizedAccessError()
        if sha256(password + user.password_salt) != user.password:
            raise UnauthorizedAccessError()

        encoded = jwt.encode(
            {"id": user.id, "email": user.email, "name": user.name},
            self.secret,
            algorithm="HS256"
        )
        return encoded

    async def authorize_user(self, ctx: Context, token: str) -> Optional[User]:
        """Authorizes user by JWT token, returns entity if token is valid"""
        try:
            decoded = jwt.decode(token, self.secret, algorithms=["HS256"])
            return await self.users.user_by_id(ctx, int(decoded['id']))
        except jwt.DecodeError:
            return None
