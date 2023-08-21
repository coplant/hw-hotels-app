from sqlalchemy import select
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.services import RoomService
from app.hotels.schemas import SFreeHotels
from app.services.base import BaseService


class HotelService(BaseService):
    model = Hotels

    @classmethod
    async def find_by_location(cls, location: str):
        async with async_session_maker() as session:
            query = select(Hotels).filter(Hotels.location.icontains(location))
            result = await session.execute(query)
            return result.scalars().all()
