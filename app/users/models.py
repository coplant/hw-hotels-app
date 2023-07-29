from sqlalchemy import Integer, Column, String

from app.database import Base


class Users(Base):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)
