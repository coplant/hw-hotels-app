from datetime import date

from app.bookings.services import BookingService
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.schemas import SFreeRooms
from app.services.base import BaseService


class RoomService(BaseService):
    model = Rooms

    @classmethod
    async def find_free_by_hotel(cls, hotel_id: int, date_from: date, date_to: date):
        hotel_rooms = await RoomService.find_all(hotel_id=hotel_id)
        result = []
        for room in hotel_rooms:
            rooms_left = await BookingService.find_free_by_id(room.id, date_from, date_to)
            result.append(
                SFreeRooms(
                    id=room.id,
                    hotel_id=hotel_id,
                    name=room.name,
                    description=room.description,
                    price=room.price,
                    services=room.services,
                    quantity=room.quantity,
                    image_id=room.image_id,
                    total_cost=room.price * (date_to - date_from).days,
                    rooms_left=rooms_left
                )
            )
        return result
