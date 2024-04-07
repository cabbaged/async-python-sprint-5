import os
from logging import config as logging_config

from pydantic import BaseSettings, PostgresDsn

from .logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    app_title: str = "LibraryApp"
    database_dsn: PostgresDsn
    project_name: str
    project_host: str
    project_port: int
    echo_db: bool
    aws_access_key_id: str
    aws_secret_access_key: str
    project_bucket: str

    class Config:
        env_file = '.env'


app_settings = AppSettings()
