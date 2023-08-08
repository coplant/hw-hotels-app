from app.services.base import BaseService
from app.users.models import Users


class UserService(BaseService):
    model = Users
