from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    postgres_url: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent /".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()