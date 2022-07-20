from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator

from app.core.utils import PostgresAsync


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SENTRY_DSN: str = ''
    ENV: str = ''
    OPENAPI_URL: str = ''

    # Postgres
    DB_ECHO_LOG: bool
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresAsync] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(  # pylint:disable=no-self-argument,no-self-use
            cls,
            v: Optional[str],
            values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresAsync.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Auth
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    class Config:
        case_sensitive = True


settings = Settings()
