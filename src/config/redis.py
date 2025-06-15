from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.config.base import BaseConfig


class RedisConfig(BaseConfig):
    """
    Configuration for Redis storage.
    """

    HOST: str = Field("localhost", description="Redis connection host")
    PORT: int = Field(6379, description="Redis connection port")
    PASSWORD: str = Field("", description="Password for Redis connection, if required")
    DB: int = Field(0, description="Database number to use in Redis")
    POOL_SIZE: int = Field(10, description="Maximum number of connections in the pool")
    TIMEOUT: int = Field(5, description="Connection timeout in seconds")

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    @property
    def url(self) -> str:
        """
        Constructs the Redis connection URL.
        """
        password_part = f":{self.PASSWORD}@" if self.PASSWORD else ""
        return f"redis://{password_part}{self.HOST}:{self.PORT}/{self.DB}"
