from sqlalchemy import Column, Integer, String, JSON

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    location: str = Column(String, nullable=False)
    services: dict = Column(JSON)
    rooms_quantity: int = Column(Integer, nullable=False)
    image_id: int = Column(Integer)
