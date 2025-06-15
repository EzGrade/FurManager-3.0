from pydantic_settings import SettingsConfigDict

from src.config.base import BaseConfig


class PostgresConfig(BaseConfig):
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str
    PASSWORD: str
    DATABASE: str

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    @property
    def async_db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"
