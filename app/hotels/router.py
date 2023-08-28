from datetime import date

from fastapi import APIRouter

from app.hotels.schemas import SFreeHotels
from app.hotels.services import HotelService
from app.hotels.rooms.router import router as rooms_router

router = APIRouter(prefix="/hotels", tags=["Hotels"])
router.include_router(rooms_router)


@router.get("")
async def get_hotels():
    return await HotelService.find_all()


@router.get("/{location}")
async def get_hotels_by_location(
        location: str, date_from: date, date_to: date
) -> list[SFreeHotels]:
    return await HotelService.find_free_by_location(location, date_from, date_to)
