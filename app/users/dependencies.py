from jose import jwt
from datetime import datetime

from starlette import status
from starlette.requests import Request
from fastapi import Depends, HTTPException

from app.config import settings
from app.users.models import Users
from app.users.services import UserService


def get_current_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_current_token)) -> Users:
    try:
        payload = jwt.decode(token, settings.security.jwt_secret_key, settings.security.jwt_algorithm)
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
