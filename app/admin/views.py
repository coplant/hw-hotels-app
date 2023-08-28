from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_exclude_list = [Users.hashed_password]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = "__all__"
    name = "Бронирование"
    name_plural = "Бронирования"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = "__all__"
    name = "Отель"
    name_plural = "Отели"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = "__all__"
    name = "Комната"
    name_plural = "Комнаты"
