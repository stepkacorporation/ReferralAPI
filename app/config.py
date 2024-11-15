import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

DEBUG: bool = os.getenv('DEBUG', 'False') == 'True'
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

if DEBUG:
    DOTENV = ROOT_DIR / 'docker/dev/.env'
else:
    DOTENV = ROOT_DIR / 'docker/prod/.env'

load_dotenv(DOTENV)


class Settings(BaseSettings):
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # JWT settings
    SECRET_KEY_ACCESS: str
    SECRET_KEY_REFRESH: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=DOTENV,
        env_file_encoding='utf-8'
    )


settings = Settings()
