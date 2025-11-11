from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "enchentes_api"
    DATABASE_URL: str
    SECRET_KEY: str = "changeme"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
