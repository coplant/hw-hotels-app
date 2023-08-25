from sqlalchemy import select, or_, and_, func, between, insert, delete

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.services.base import BaseService


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def find_free_by_id(cls, room_id, date_from, date_to):
        async with async_session_maker() as session:
            booked_rooms = select(func.count()).where(
                and_(
                    cls.model.room_id == room_id,
                    or_(
                        between(date_to, cls.model.date_from, cls.model.date_to),
                        between(date_from, cls.model.date_from, cls.model.date_to),
                        between(cls.model.date_from, date_from, date_to),
                        between(cls.model.date_to, date_from, date_to)
                    )
                )
            ).as_scalar()
            get_rooms_left = select(
                func.coalesce(Rooms.quantity - booked_rooms, Rooms.quantity)).where(
                Rooms.id == room_id
            )
            result = await session.execute(get_rooms_left)
            return result.scalar()

    @classmethod
    async def add(cls, user_id, room_id, date_from, date_to):
        rooms_left: int = await BookingService.find_free_by_id(room_id, date_from, date_to)
        async with async_session_maker() as session:
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                result = await session.execute(get_price)
                price: int = result.scalar()
                add_booking = insert(cls.model).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(cls.model)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def delete(cls, current_user, booking_id: int):
        async with async_session_maker() as session:
            delete_query = delete(cls.model).where(
                and_(
                    cls.model.id == booking_id,
                    cls.model.user_id == current_user.id
                )
            ).returning(cls.model.id)
            delete_booking = await session.execute(delete_query)
            await session.commit()
            return delete_booking.scalar()
