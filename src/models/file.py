from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class File(Base):
    __tablename__ = "file"
    id = Column(String(), primary_key=True)
    username = Column(String(), nullable=False)
    name = Column(String(), nullable=False)
    path = Column(String(), unique=True)
    created_at = Column(String(), index=True, default=datetime.utcnow)
    size = Column(Integer)
    is_downloadable = Column(Boolean, default=True)
