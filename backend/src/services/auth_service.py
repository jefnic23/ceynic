from datetime import UTC, datetime, timedelta
from hashlib import sha256
from hmac import compare_digest, new as hmac_new
from typing import Annotated

from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from src.config import Settings, get_settings
from src.database import ASYNC_SESSION_DEPENDENCY
from src.exceptions import credentials_exception
from src.models.refresh_token import RefreshToken
from src.models.user import User
from src.services.refresh_tokens_service import RefreshTokensService
from src.services.users_service import UsersService


class AuthService:
    def __init__(
        self,
        session: ASYNC_SESSION_DEPENDENCY,
        settings: Annotated[Settings, Depends(get_settings)],
        users_service: Annotated[UsersService, Depends()],
        refresh_tokens_service: Annotated[RefreshTokensService, Depends()],
    ):
        self._session = session
        self._settings = settings
        self._users_service = users_service
        self._refresh_tokens_service = refresh_tokens_service

    async def authenticate_user(self, email: str, password: str) -> User | bool:
        user = await self._users_service.get_user_by_email(email=email)
        if not user:
            return False
        if not user.verify_password(secret=password):
            return False
        return user

    def generate_access_token(self, sub: int, expiry_minutes: int = 5) -> str:
        exp = datetime.now(UTC) + timedelta(minutes=expiry_minutes)
        claims = {
            "exp": exp,
            "sub": str(sub),
            "purpose": "access",
        }
        return jwt.encode(
            claims=claims,
            key=self._settings.SECRET_KEY,
            algorithm="HS256",
        )

    async def generate_refresh_token(self, sub: int, expiry_minutes: int = 43200) -> str:
        exp = datetime.now(UTC) + timedelta(minutes=expiry_minutes)
        claims = {
            "exp": exp,
            "sub": str(sub),
            "purpose": "refresh",
        }
        token = jwt.encode(
            claims=claims,
            key=self._settings.SECRET_KEY,
            algorithm="HS256",
        )
        refresh_token = await self._refresh_tokens_service.get_refresh_token(user_id=sub)
        if not refresh_token:
            refresh_token = RefreshToken(token=token, expiry_time=exp, user_id=sub)
            self._session.add(refresh_token)
        else:
            refresh_token.token = token
            refresh_token.expiry_time = exp
        await self._session.commit()
        return token

    def generate_reset_token(self, user: User, expiry_minutes: int = 30) -> str:
        claims = {
            "exp": datetime.now(UTC) + timedelta(minutes=expiry_minutes),
            "sub": str(user.id),
            "purpose": "reset",
            "password_version": self._password_version(user),
        }
        return jwt.encode(claims=claims, key=self._settings.SECRET_KEY, algorithm="HS256")

    def _password_version(self, user: User) -> str:
        return hmac_new(self._settings.SECRET_KEY.encode(), user.password.encode(), sha256).hexdigest()

    async def verify_reset_token(self, token: str) -> User:
        payload = self.verify_token(token, purpose="reset")
        user = await self._users_service.get_user_by_id(int(payload["sub"]))
        version = payload.get("password_version")
        if not user or not isinstance(version, str) or not compare_digest(version, self._password_version(user)):
            raise credentials_exception
        return user

    async def verify_refresh_token(self, token: str) -> int:
        payload = self.verify_token(token, purpose="refresh")
        user_id = int(payload["sub"])
        stored_token = await self._refresh_tokens_service.get_refresh_token(user_id=user_id)
        if not stored_token or not compare_digest(stored_token.token, token):
            raise credentials_exception
        if not await self._users_service.get_user_by_id(user_id):
            raise credentials_exception
        return user_id

    def verify_token(
        self, token: str, purpose: str = "access", exception: HTTPException = credentials_exception
    ) -> dict[str, object]:
        try:
            payload = jwt.decode(token, self._settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("sub")
            if (
                not isinstance(user_id, str)
                or not user_id.isdecimal()
                or payload.get("purpose") != purpose
            ):
                raise exception
        except JWTError:
            raise exception
        return payload
