import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field


class FileBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    created_at: Optional[datetime.datetime]
    size: int
    path: str
    is_downloadable: bool = True


class FileCreate(FileBase):
    username: str


class FileUpdate(FileCreate):
    pass


class FileResponse(FileBase):
    username: str

    class Config:
        orm_mode = True
