from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette import status

from src.schemas.token import Token
from src.schemas.token_refresh_request import TokenRefreshRequest
from src.services.auth_service import AuthService
from src.services.messages_service import MessagesService
from src.services.users_service import UsersService

router = APIRouter()


@router.post("/login")
async def login(
    auth_service: Annotated[AuthService, Depends()],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await auth_service.authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.generate_access_token(sub=user.id)
    refresh_token = await auth_service.generate_refresh_token(sub=user.id)
    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)


@router.post("/refresh")
async def refresh_access(
    auth_service: Annotated[AuthService, Depends()],
    body: TokenRefreshRequest,
) -> Token:
    user_id = await auth_service.verify_refresh_token(body.refresh_token)
    access_token = auth_service.generate_access_token(sub=user_id)
    refresh_token = await auth_service.generate_refresh_token(sub=user_id)
    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)


@router.post("/reset_password")
async def reset_password_request(
    email: Annotated[EmailStr, Form()],
    users_service: Annotated[UsersService, Depends()],
    auth_service: Annotated[AuthService, Depends()],
    messages_service: Annotated[MessagesService, Depends()],
) -> JSONResponse:
    user = await users_service.get_user_by_email(email)
    if not user:
        return JSONResponse("Email sent.")
    token = auth_service.generate_reset_token(user)
    subdomain = await users_service.get_subdomain_from_user(user.id)
    if subdomain is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Storefront not found")
    messages_service.send_reset_password_message(email, token, subdomain)
    return JSONResponse("Email sent.")

@router.post("/reset_password/{token:str}")
async def reset_password(
    token: str,
    password: Annotated[str, Form(min_length=8)],
    users_service: Annotated[UsersService, Depends()],
    auth_service: Annotated[AuthService, Depends()],
) -> JSONResponse:
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password must be at most 72 bytes")
    user = await auth_service.verify_reset_token(token)
    await users_service.update_password(user.id, password)
    return JSONResponse("Your password has been reset.")
