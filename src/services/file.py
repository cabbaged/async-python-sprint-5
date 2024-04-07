from models.file import File as FileModel
from schemas.file_schema import FileCreate, FileUpdate

from .base import RepositoryDB


class RepositoryFile(RepositoryDB[FileModel, FileCreate, FileUpdate]):
    pass


file_crud = RepositoryFile(FileModel)
