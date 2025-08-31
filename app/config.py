from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    database_user: str
    database_host: str
    database_port: str
    database_password: str
    database_name: str

    secret_key: str = "sadjfljalsjfdljasljfdlajsd"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
