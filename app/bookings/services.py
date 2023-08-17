from sqlalchemy import select, or_, and_, func, between, insert

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Rooms
from app.services.base import BaseService


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def add(cls, user_id, room_id, date_from, date_to):
        async with async_session_maker() as session:
            booked_rooms = select(func.count()).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        between(date_to, Bookings.date_from, Bookings.date_to),
                        between(date_from, Bookings.date_from, Bookings.date_to),
                        between(Bookings.date_from, date_from, date_to),
                        between(Bookings.date_to, date_from, date_to)
                    )
                )
            ).as_scalar()
            get_rooms_left = select(func.coalesce(Rooms.quantity - booked_rooms, Rooms.quantity))

            result = await session.execute(get_rooms_left)
            rooms_left: int = result.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                result = await session.execute(get_price)
                price: int = result.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
