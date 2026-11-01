from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_name: str = "ThittamTrack"
    environment: str = "local"

    # Any OpenAI-compatible Chat Completions endpoint can be used.
    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_primary_model: str = "gpt-4o-mini"
    llm_fallback_model: str = "gpt-4.1-mini"
    llm_timeout_seconds: float = 35.0
    llm_max_retries: int = 2

    # USD per 1 million tokens. Override these for the selected provider/models.
    primary_input_usd_per_million: float = 0.15
    primary_output_usd_per_million: float = 0.60
    fallback_input_usd_per_million: float = 0.40
    fallback_output_usd_per_million: float = 1.60

    database_url: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
