from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str  # Railway provides this as DATABASE_URL

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
