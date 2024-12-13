from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
from pydantic import validator, ValidationError
import re


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Personal Finance Manager"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    MYSQL_URI: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Email Settings (for future use)
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_TLS: bool = True
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("MYSQL_URI")
    def validate_mysql_uri(cls, v):
        pattern = re.compile(
            r"mysql://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:/]+)(?::(?P<port>\d+))?/(?P<database>[^?]+)"
        )
        if not pattern.match(v):
            raise ValueError("Invalid MYSQL_URI format")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
