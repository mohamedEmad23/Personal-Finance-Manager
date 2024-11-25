# import os
# from pydantic import BaseSettings
# from pydantic.v1 import BaseSettings
#
#
#
# class Settings(BaseSettings):
#     DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql://root:123Main_Connection123@localhost/finance_manager_sp")
#     SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#
#
# settings = Settings()
from pydantic import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Personal Finance Manager"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Email Settings (for future use)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
