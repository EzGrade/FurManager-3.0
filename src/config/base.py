from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    """
    Base configuration class for the application.
    Inherits from BaseSettings to manage environment variables.
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"
