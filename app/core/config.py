import secrets
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    # Load environment from .env file if present
    load_dotenv()

    # Very secret
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # Database
    SQLALCHEMY_DATABASE_URI: str
    # MUH ADMIN
    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_EMAIL: EmailStr

    # JWT and Login specifics
    # minutes, hours, days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14
    COOKIE_EXPIRATION: int = 60 * 60 * 24 * 14
    JWT_SECRET: str
    ALGORITHM: str = "HS256"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
