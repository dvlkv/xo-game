from context import Context
from modules import UnauthorizedAccessError
from ..user import Users
from utils import sha256
import jwt

AUTH_SECRET = "some secret that should be stored in config or env var"


class AuthModule:
    async def authorize_user(self, ctx: Context, email: str, password: str) -> str:
        user = await Users.user_by_email(ctx, email)
        if not user:
            raise UnauthorizedAccessError()
        if sha256(password + user.password_salt) != user.password:
            raise UnauthorizedAccessError()

        encoded = jwt.encode(
            {"id": user.id, "email": user.email, "name": user.name},
            AUTH_SECRET,
            algorithm="HS256"
        )
        return encoded
