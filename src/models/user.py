from typing import TYPE_CHECKING, ClassVar, Optional

from passlib.context import CryptContext
from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.refresh_token import RefreshToken
    from src.models.storefront import Storefront


class UserBase(BaseModel):
    PASSWORD_CONTEXT: ClassVar[CryptContext] = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    email: str = Field(unique=True)
    first_name: str | None = None
    last_name: str | None = None
    password: str

    storefront_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("storefronts.id", ondelete="CASCADE"), nullable=False
        )
    )

    def verify_password(self, secret: str, password_context: CryptContext = PASSWORD_CONTEXT) -> bool:
        return password_context.verify(secret=secret, hash=self.password)

    def set_password(self, secret: str, password_context: CryptContext = PASSWORD_CONTEXT) -> None:
        self.password = password_context.hash(secret=secret)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    
    storefront: "Storefront" = Relationship(back_populates="users")
    refresh_token: Optional["RefreshToken"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
