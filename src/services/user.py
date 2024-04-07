from models.user import User as UserModel
from schemas.user_schema import User, UserCreate

from .base import RepositoryDB


class RepositoryUser(RepositoryDB[User, UserCreate, UserCreate]):
    pass


user_crud = RepositoryUser(UserModel)
