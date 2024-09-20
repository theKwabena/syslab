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
    PROJECT_NAME: str = ""
    PROJECT_API_VERSION: str = "/api/v1"
    DOCKER_HOST_URL: str = "tcp://192.168.1.154:2376"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = ["http://localhost:3000", "http://localhost:8000", 'http://192.254.0.115:3000']

    DB_URL: str
    # ------------------------------------------------------------
    # security config definitions
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 12  # 12 days

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    model_config = SettingsConfigDict(
        env_file='.env'
    )


# ------------------------------------------------------------
@lru_cache
def get_settings() -> Settings:
    return Settings()


# ------------------------------------------------------------
settings = get_settings()
