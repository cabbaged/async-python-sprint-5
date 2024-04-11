from models.user import User as UserModel
from schemas.user_schema import UserCreate

from .base import RepositoryDB


class RepositoryUser(RepositoryDB[UserModel, UserCreate, UserCreate]):
    pass


user_crud = RepositoryUser(UserModel)
