from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey


class Rooms(Base):
    __tablename__ = "rooms"
    id: int = Column(Integer, primary_key=True)
    hotel_id: int = Column(ForeignKey("hotels.id"))
    name: str = Column(String, nullable=False)
    description: str = Column(String)
    price: int = Column(Integer, nullable=False)
    services: list[str] = Column(JSON)
    quantity: int = Column(Integer, nullable=False)
    image_id: int = Column(Integer)

    bookings = relationship("Bookings", back_populates="room")
    hotel = relationship("Hotels", back_populates="rooms")

    def __str__(self):
        return self.name
