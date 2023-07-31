from fastapi import APIRouter

from app.bookings.schemas import SBooking
from app.bookings.services import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings() -> list[SBooking]:
    bookings = await BookingService.find_all()
    return bookings

