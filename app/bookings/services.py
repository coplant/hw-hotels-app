from app.bookings.models import Bookings
from app.services.base import BaseService


class BookingService(BaseService):
    model = Bookings
