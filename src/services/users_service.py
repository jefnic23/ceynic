from fastapi import HTTPException
from sqlalchemy import delete
from sqlmodel import select
from starlette import status

from src.database import ASYNC_SESSION_DEPENDENCY
from src.models.refresh_token import RefreshToken
from src.models.storefront import Storefront
from src.models.user import User


class UsersService:
    def __init__(self, session: ASYNC_SESSION_DEPENDENCY):
        self._session = session

    async def get_user_by_id(self, id: int) -> User | None:
        statement = select(User).where(User.id == id)
        result = await self._session.exec(statement=statement)
        return result.one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self._session.exec(statement=statement)
        return result.one_or_none()

    async def get_subdomain_from_user(self, id: int) -> str | None:
        statement = select(Storefront.subdomain).join(User, User.storefront_id == Storefront.id).where(User.id == id)
        result = await self._session.exec(statement=statement)
        return result.one_or_none()

    async def update_password(self, id: int, password: str) -> None:
        user = await self.get_user_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user.set_password(password)
        self._session.add(user)
        await self._session.exec(delete(RefreshToken).where(RefreshToken.user_id == id))
        await self._session.commit()
