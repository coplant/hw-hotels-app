from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app import exceptions as ex
from app.users.auth import get_hashed_password, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
from app.users.services import UserService

router = APIRouter(tags=["Users"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserAuth):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise ex.UserAlreadyExistsException
    hashed_password = get_hashed_password(user_data.password)
    user_id = await UserService.add(email=user_data.email, hashed_password=hashed_password)
    if not user_id:
        raise ex.BookingException()
    return {"id": user_id}


@router.post("/login")
async def login_user(user_data: SUserAuth, response: Response):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise ex.InvalidEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")


@router.get("/me")
async def get_user_me(current_user: Users = Depends(get_current_user)):
    return current_user
