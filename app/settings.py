from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Campus Compass API"
    debug: bool = False
    environment: str
    database_uri: str

    model_config = SettingsConfigDict(env_file=".env")
