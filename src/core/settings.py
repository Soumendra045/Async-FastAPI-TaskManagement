from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

file_path = Path(__file__).resolve().parent.parent / ".env/.env"

class Settings(BaseSettings):
    """Settings for the application"""
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_PORT: int

    model_config = SettingsConfigDict(
        env_file=file_path,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()