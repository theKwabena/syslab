# Stdlib imports
import secrets
from functools import lru_cache
from typing_extensions import Self

# Third party imports
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, computed_field, model_validator


class Settings(BaseSettings):
    # ------------------------------------------------------------
    # project config definitions
    DOMAIN: str = "localhost"
    PROJECT_NAME: str = ""
    PROJECT_API_VERSION: str = "/api/v1"
    DOCKER_HOST_URL : str = "tcp://192.168.1.154:2376"

    # ------------------------------------------------------------
    # security config definitions
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 12  # 12 days
    CORS_ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000", 'http://192.254.0.115:3000']


# ------------------------------------------------------------
@lru_cache
def get_settings() -> Settings:
    return Settings()


# ------------------------------------------------------------
settings = get_settings()