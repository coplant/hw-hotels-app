from datetime import date

from sqlalchemy import Integer, Column, Date, ForeignKey, Computed
from sqlalchemy.orm import relationship

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"
    id: int = Column(Integer, primary_key=True)
    room_id: int = Column(ForeignKey("rooms.id"))
    user_id: int = Column(ForeignKey("users.id"))
    date_from: date = Column(Date, nullable=False)
    date_to: date = Column(Date, nullable=False)
    price: int = Column(Integer, nullable=False)
    total_cost: int = Column(Integer, Computed("(date_to - date_from) * price"))
    total_days: int = Column(Integer, Computed("date_to - date_from"))

    room = relationship("Rooms", back_populates="bookings")
    user = relationship("Users", back_populates="hotels")

    def __str__(self):
        return f"Бронирование #{self.id}"
