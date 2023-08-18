from app.hotels.rooms.models import Rooms
from app.services.base import BaseService


class RoomService(BaseService):
    model = Rooms
