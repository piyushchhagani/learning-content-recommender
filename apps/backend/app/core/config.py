from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Learning Content Recommender"
    app_env: str = "development"
    debug: bool = True

    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    database_url: str = ""
    redis_url: str = ""

    youtube_api_key: str = ""
    recommendation_min_score: float = 30.0

    llm_api_key: str = ""
    llm_model: str = ""

    secret_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()