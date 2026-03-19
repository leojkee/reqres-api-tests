from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    BASE_URL: str = "https://dummyjson.com"
    DEFAULT_TIMEOUT: int = 30
    TEST_USERNAME: str = "emilys"
    TEST_PASSWORD: str = "emilyspass"

    ADMIN_USERNAME: str = "michaelw"
    ADMIN_PASSWORD: str = "michaelwpass"

    DATABASE_URL: str = "postgresql://reqres:reqres_secret@localhost:5432/reqres_test"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    ENCRYPTION_KEY: str = ""

    model_config = {
        "env_file": BASE_DIR / ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
