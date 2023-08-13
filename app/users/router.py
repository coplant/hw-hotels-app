from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import Response

from app.users.auth import get_hashed_password, authenticate_user, create_access_token
from app.users.schemas import SUserAuth
from app.users.services import UserService

router = APIRouter(tags=["Users"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserAuth):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    hashed_password = get_hashed_password(user_data.password)
    user_id = await UserService.add(email=user_data.email, hashed_password=hashed_password)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return {"id": user_id}


@router.post("/login")
async def login_user(user_data: SUserAuth, response: Response):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
