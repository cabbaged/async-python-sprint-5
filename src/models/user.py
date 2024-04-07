from sqlalchemy import Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(), unique=True, nullable=False)
    hashed_password = Column(String(), nullable=False)
