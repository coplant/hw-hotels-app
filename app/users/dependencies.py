from jose import jwt
from datetime import datetime

from fastapi import Depends
from fastapi.requests import Request

from app import exceptions as ex
from app.config import settings
from app.users.models import Users
from app.users.services import UserService


def get_current_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise ex.TokenNotFoundException
    return token


async def get_current_user(token: str = Depends(get_current_token)) -> Users:
    try:
        payload = jwt.decode(token, settings.security.jwt_secret_key, settings.security.jwt_algorithm)
    except jwt.JWTError:
        raise ex.TokenNotValidException
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise ex.TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise ex.UserNotFoundException
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise ex.UserNotFoundException
    return user
