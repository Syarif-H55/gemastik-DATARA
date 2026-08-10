"""Konfigurasi aplikasi DATARA.

Membaca variabel lingkungan dari file `.env` (root backend/).
Semua nilai penting diakses melalui `get_settings()` agar ter-cache.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "DATARA API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"

    database_url: str = "mysql+pymysql://root:password@localhost:3306/datara"

    # Fallback terpisah (dipakai bila database_url tidak diset).
    db_user: str = "root"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "datara"

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
