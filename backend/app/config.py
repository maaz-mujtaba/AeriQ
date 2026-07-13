from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL : str
    OPEN_METEO_BASE_URL : str
    APP_NAME : str
    DEBUG = Optional[bool] = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
settings = Settings()