import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str

    class config:
        # model_config = SettingsConfigDict(env_file=".env")
        env_file = ".env" if os.getenv("ENV") != "prod" else None


settings = Settings()
