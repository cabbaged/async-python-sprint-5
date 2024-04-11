from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class File(Base):
    __tablename__ = "file"
    id = Column(String(64), primary_key=True)
    username = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    path = Column(String(255), unique=True)
    created_at = Column(String(64), index=True, default=datetime.utcnow)
    size = Column(Integer)
    is_downloadable = Column(Boolean, default=True)
