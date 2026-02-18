from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


class BotConfig(BaseConfig):
    BOT_TOKEN: str


class DatabaseConfig(BaseConfig):
    DB_PATH: str = f"sqlite:///{BASE_DIR / 'database.sqlite'}"


class ApiConfig(BaseConfig):
    JOOBLE_API_KEY: str
