from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class User(UserBase):
    password: str


class UserCreate(UserBase):
    hashed_password: str


class UserResponse(UserBase):
    class Config:
        orm_mode = True
