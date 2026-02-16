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
    LOGIN_USER: str
    PASSWORD: str
    SERVERNAME: str
    DBNAME: str
    DRIVER: str

    def pg_dsn(self) -> str:
        return (
            f"postgresql+{self.DRIVER}://{self.LOGIN_USER}:{self.PASSWORD}"
            f"@{self.SERVERNAME}/{self.DBNAME}"
        )
