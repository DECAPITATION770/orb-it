from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DB_URL: str
    DEBUG: bool = True

    @computed_field
    @property
    def docs_url(self) -> str | None:
        return "/docs" if self.DEBUG else None

    @computed_field
    @property
    def redoc_url(self) -> str | None:
        return "/redoc" if self.DEBUG else None

    @computed_field
    @property
    def openapi_url(self) -> str | None:
        return "/openapi.json" if self.DEBUG else None

    #JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    SECRET_KEY: str = "AShdkjaslie"
    JWT_ALGORITHM: str = "HS256"

settings = Settings()