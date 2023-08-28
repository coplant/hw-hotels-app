from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)

    hotels = relationship("Bookings", back_populates="user")

    def __str__(self):
        return self.email
