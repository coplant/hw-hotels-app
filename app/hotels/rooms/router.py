from datetime import date
from fastapi import APIRouter

from app.hotels.rooms.services import RoomService
from app.hotels.rooms.schemas import SFreeRooms

router = APIRouter()


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_hotel(
        hotel_id: int, date_from: date, date_to: date
) -> list[SFreeRooms]:
    return await RoomService.find_free_by_hotel(hotel_id, date_from, date_to)
