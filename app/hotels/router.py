from fastapi import APIRouter

from app.hotels.services import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels():
    return await HotelService.find_all()
