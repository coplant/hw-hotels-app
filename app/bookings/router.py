from datetime import date

from fastapi import APIRouter, Depends, status

from app import exceptions as ex
from app.bookings.schemas import SUserBooking
from app.bookings.services import BookingService
from app.hotels.rooms.services import RoomService
from app.hotels.services import HotelService
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SUserBooking]:
    bookings = await BookingService.find_all(user_id=user.id)
    result = []
    for booking in bookings:
        room = await RoomService.find_by_id(booking.room_id)
        hotel = await HotelService.find_by_id(room.hotel_id)
        result.append(
            SUserBooking(
                id=booking.id,
                room_id=booking.room_id,
                user_id=booking.user_id,
                date_from=booking.date_from,
                date_to=booking.date_to,
                price=booking.price,
                total_cost=booking.total_cost,
                total_days=booking.total_days,
                image_id=hotel.image_id,
                name=hotel.name,
                description=room.description,
                services=hotel.services,
            )
        )
    return result


@router.post("")
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise ex.NoRoomAvailableException
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking = await BookingService.delete(user, booking_id)
    if not booking:
        raise ex.NotFoundException
    return booking
