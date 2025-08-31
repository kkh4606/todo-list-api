from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_user: str
    database_host: str
    database_port: str
    database_password: str
    database_name: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
