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
    DB_PATH: str = str(BASE_DIR / "database.sqlite")

    def sqlite_dsn(self) -> str:
        """Return the SQLAlchemy SQLite DSN."""
        return f"sqlite:///{self.DB_PATH}"
