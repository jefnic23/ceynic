from pathlib import Path
from typing import Annotated
from urllib.parse import urlencode

from fastapi import BackgroundTasks, Depends, HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from sqlmodel import select

from src.config import Settings, get_settings
from src.database import ASYNC_SESSION_DEPENDENCY
from src.models.storefront import Storefront
from src.models.user import User


class MessagesService:
    def __init__(
        self,
        settings: Annotated[Settings, Depends(get_settings)],
        background_tasks: BackgroundTasks,
        session: ASYNC_SESSION_DEPENDENCY,
    ):
        self._settings: Settings = settings
        self._background_tasks = background_tasks
        self._session = session

    async def send_contact_message(self, name: str, email: str, message: str, subdomain: str) -> None:
        statement = (
            select(User.email)
            .join(Storefront, User.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
        )
        result = await self._session.exec(statement)
        recipients = result.all()
        if not recipients:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Storefront contact not found")

        fast_mail = self._get_fast_mail(from_email=email, from_name=name)
        mail_message = MessageSchema(
            subject=f"Message from {name}",
            recipients=recipients,
            template_body={"message": message},
            subtype=MessageType.html,
        )
        self._background_tasks.add_task(fast_mail.send_message, mail_message, "contact.html")

    def send_reset_password_message(self, email: str, token: str, subdomain: str) -> None:
        fast_mail = self._get_fast_mail(self._settings.MAILGUN_SMTP_LOGIN)
        origin = self._settings.STOREFRONT_ORIGIN_TEMPLATE.format(subdomain=subdomain).rstrip("/")
        reset_url = f"{origin}/reset-password?{urlencode({'token': token})}"
        message = MessageSchema(
            subject="Reset Password Request",
            recipients=[email],
            template_body={"reset_url": reset_url},
            subtype=MessageType.html,
        )
        self._background_tasks.add_task(fast_mail.send_message, message, "reset_password.html")

    def _get_fast_mail(self, from_email: str, from_name: str | None = None) -> FastMail:
        connection_config = self._get_connection_config(from_email, from_name)
        return FastMail(connection_config)

    def _get_connection_config(self, from_email: str, from_name: str | None = None) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=self._settings.MAILGUN_SMTP_LOGIN,
            MAIL_PASSWORD=self._settings.MAILGUN_SMTP_PASSWORD,
            MAIL_PORT=self._settings.MAILGUN_SMTP_PORT,
            MAIL_SERVER=self._settings.MAILGUN_SMTP_SERVER,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            MAIL_FROM=from_email,
            MAIL_FROM_NAME=from_name,
            TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
        )
