from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Campus Compass API"
    DEBUG: bool = False
    ENVIRONMENT: str
    DATABASE_URI: str

    model_config = SettingsConfigDict(env_file=".env")
