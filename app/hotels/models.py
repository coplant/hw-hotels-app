from sqlalchemy import Column, Integer, String, JSON, ForeignKey

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    location: str = Column(String, nullable=False)
    services: dict = Column(JSON)
    rooms_quantity: int = Column(Integer, nullable=False)
    image_id: int = Column(Integer)


class Rooms(Base):
    __tablename__ = "rooms"
    id: int = Column(Integer, primary_key=True)
    hotel_id: int = Column(ForeignKey("hotels.id"))
    name: str = Column(String, nullable=False)
    description: str = Column(String)
    price: int = Column(Integer, nullable=False)
    services: dict = Column(JSON)
    quantity: int = Column(Integer, nullable=False)
    image_id: int = Column(Integer)
