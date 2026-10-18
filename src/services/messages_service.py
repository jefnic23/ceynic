from pathlib import Path
from typing import Annotated
from urllib.parse import urlencode

from fastapi import BackgroundTasks, Depends
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.config import Settings, get_settings


class MessagesService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)], background_tasks: BackgroundTasks):
        self._settings: Settings = settings
        self._background_tasks = background_tasks

    def send_contact_message(self, name: str, email: str, message: str) -> None:
        fast_mail = self._get_fast_mail(from_email=email, from_name=name)
        mail_message = MessageSchema(
            subject=f"Message from {name}",
            recipients=[self._settings.RECIPIENT_EMAIL],  # todo: pull this from DB storefront
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
            MAIL_FROM=from_email,
            MAIL_FROM_NAME=from_name,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
        )
