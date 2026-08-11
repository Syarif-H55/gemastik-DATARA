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

    # URL koneksi MySQL. Wajib diset lewat environment (.env / secret manager).
    # Tidak ada default kredensial di source code.
    database_url: str = ""

    # Fallback (dipakai bila DATABASE_URL tidak diset). Kredensial tidak
    # di-hardcode; nilai kosong akan membuat koneksi gagal dengan jelas.
    db_user: str = ""
    db_password: str = ""
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = ""

    # Origin yang diizinkan CORS (dipisahkan koma).
    cors_origins: str = "http://localhost:3000"

    # Authentication: JWT access token (stateless, Bearer).
    # Wajib diset lewat environment; tidak ada default secret di source code.
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 1 hari

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if not self.db_user or not self.db_name:
            raise RuntimeError(
                "DATABASE_URL (atau DB_USER/DB_NAME) belum dikonfigurasi. "
                "Salin .env.example menjadi .env dan isi koneksi MySQL."
            )
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def resolved_jwt_secret(self) -> str:
        if not self.jwt_secret:
            raise RuntimeError(
                "JWT_SECRET belum dikonfigurasi. "
                "Isi .env dengan secret acak (minimal 32 karakter)."
            )
        return self.jwt_secret

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
