from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "engineering-knowledge-assistant"
    environment: str = "development"
    log_level: str = "INFO"
    agent_enabled: bool = True

    gemini_api_key: str = ""
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "engineering_knowledge"
    embedding_dimension: int = 768
    knowledge_dir: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
