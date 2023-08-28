from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Column, Integer, String, JSON


class Hotels(Base):
    __tablename__ = "hotels"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    location: str = Column(String, nullable=False)
    services: list[str] = Column(JSON)
    rooms_quantity: int = Column(Integer, nullable=False)
    image_id: int = Column(Integer)

    rooms = relationship("Rooms", back_populates="hotel")

    def __str__(self):
        return self.name
