from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "engineering-knowledge-assistant"
    environment: str = "development"
    log_level: str = "INFO"
    agent_enabled: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
