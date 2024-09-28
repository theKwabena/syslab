# Stdlib imports
import secrets
from functools import lru_cache
from typing_extensions import Self
from typing import Annotated, Any

# Third party imports
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    # ------------------------------------------------------------
    # project config definitions
    DOMAIN: str = "localhost"
    PROJECT_NAME: str = "UITS SYSLAB BACKEND"
    PROJECT_API_VERSION: str = "/api/v1"
    DOCKER_HOST_URL: str = "tcp://192.168.1.154:2376"

    WEB_PORT_END: int = 9000
    DNS_PORT_END: int = 6000
    DNS_PORT_START: int = 5500
    WEB_PORT_START: int = 8100

    ADMIN_USER: str
    ADMIN_PASSWORD: str

    DOCKER_REPO_USER: str
    DOCKER_REPO_URL: str
    DEFAULT_UNIX_IMAGE: str
    DOCKER_REPO_PASSWORD: str

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = ["http://localhost:3000", "http://localhost:8000", 'http://192.254.0.115:3000']

    # ------------------------------------------------------------
    # security config definitions
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 12  # 12 days

    model_config = SettingsConfigDict(
        env_file='.env'
    )


# ------------------------------------------------------------
@lru_cache
def get_settings() -> Settings:
    return Settings()


# ------------------------------------------------------------
settings = get_settings()
