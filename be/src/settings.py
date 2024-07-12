from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from string import Template


class RabbitConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file="be.env")

    RABBIT_CONFIG: RabbitConfig

    RETRIEVE_DATA_QUEUE_NAME: Template = Template("retrieve_data_for_$key")
    UPLOAD_DATA_QUEUE_NAME: str = "upload_data"
    DOWNLOAD_DATA_QUEUE_NAME: str = "download_data"


def get_settings() -> Settings:
    return Settings()
