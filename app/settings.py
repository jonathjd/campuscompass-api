from pydantic import BaseSettings, AnyHttpUrl, validator
import json


class Settings(BaseSettings):
    APP_NAME: str = "Campus Compass API"
    DATABASE_URI: str
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError(
                    "BACKEND_CORS_ORIGINS must be a valid JSON-formatted list of origins"
                )
        elif isinstance(v, list):
            return v
        raise ValueError(
            "BACKEND_CORS_ORIGINS must be a list or a JSON-formatted string"
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
