"""
Application settings loaded from environment variables.
All secrets come from .env — never hardcoded here.
"""
from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────
    environment: Literal["development", "staging", "production"] = "development"
    app_name: str = "ResumeMaker"
    app_version: str = "0.1.0"
    debug: bool = False

    # ── Database ─────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://resumemaker:resumemaker_dev@localhost:5432/resumemaker"

    # ── Security ─────────────────────────────────────────
    secret_key: str = "CHANGE_ME_generate_with_secrets_token_hex_32"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # ── CORS ─────────────────────────────────────────────
    backend_cors_origins: list[str] = ["http://localhost:3000"]

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # ── AI ───────────────────────────────────────────────
    llm_provider: Literal["gemini", "openai"] = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # ── Storage ──────────────────────────────────────────
    storage_provider: Literal["local", "s3"] = "local"
    local_storage_path: str = "./uploads"

    # S3 (optional, for production)
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_s3_bucket: str = ""
    aws_region: str = "us-east-1"

    # ── File Upload Limits ───────────────────────────────
    max_upload_size_bytes: int = 10 * 1024 * 1024  # 10 MB
    allowed_upload_extensions: list[str] = [".docx", ".pdf"]

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
