from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import Response

from app.users.auth import get_hashed_password
from app.users.schemas import SUserRegister
from app.users.services import UserService

router = APIRouter(tags=["Users"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserRegister):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    hashed_password = get_hashed_password(user_data.password)
    user_id = await UserService.add(email=user_data.email, hashed_password=hashed_password)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return {"id": user_id}


@router.post("/login")
async def login_user():
    ...
