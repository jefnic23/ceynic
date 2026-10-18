from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from src.dependencies import verify_recaptcha
from src.services.messages_service import MessagesService

router = APIRouter()


@router.post("/contact", dependencies=[Depends(verify_recaptcha)])
async def send_contact_email(
    name: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    message: Annotated[str, Form()],
    messages_service: Annotated[MessagesService, Depends()],
) -> JSONResponse:
    messages_service.send_contact_message(name, email, message)

    return JSONResponse("Email sent.")
