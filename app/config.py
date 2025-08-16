import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        # model_config = SettingsConfigDict(env_file=".env")
        env_file = ".env" if os.getenv("ENV") != "prod" else None


settings = Settings()
