"""
Application Settings & Environment Configuration
Using Pydantic BaseSettings for strongly-typed configuration management.
"""

from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Information
    APP_NAME: str = "Livelihood-Assistant-AI"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Server Binding
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # API Prefix
    API_V1_PREFIX: str = "/v1"

    # Security & CORS
    ALLOWED_ORIGINS: Union[str, List[str]] = ["*"]

    # AI & Speech Services (Credentials loaded strictly from env)
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key")
    BHASHINI_API_KEY: str = Field(default="", description="Bhashini ASR/TTS API key")
    BHASHINI_USER_ID: str = Field(default="", description="Bhashini User identifier")
    BHASHINI_PIPELINE_ID: str = Field(default="", description="Bhashini Pipeline identifier")

    # Regional / Rules Data Storage
    DATA_DIR: str = "./data"
    SEED_DATA_DIR: str = "./data/seed"

    # Skill normalization.  Fuzzy candidates below this threshold are UNKNOWN.
    SKILL_NORMALIZATION_MIN_CONFIDENCE: float = Field(default=0.90, ge=0.0, le=1.0)
    SKILL_NORMALIZATION_PHRASE_CONFIDENCE: float = Field(default=0.95, ge=0.0, le=1.0)

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: Union[str, List[str]]) -> List[str]:
        if isinstance(value, str):
            if value.strip() == "*":
                return ["*"]
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
