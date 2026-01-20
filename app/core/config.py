from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Segurança
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Banco de dados
    DATABASE_URL: str

    class Config:
        env_file = (
            ".env.test"
            if Path(".env.test").exists()
            else ".env"
        )

settings = Settings()
