"""Error domain DATARA.

Semua error yang dilempar layer bisnis mewarisi :class:`AppError`.
Status code dan body dikonversi menjadi struktur respons konsisten
``{"success": false, "message": ..., "errors": ...}`` oleh exception handler.
"""


class AppError(Exception):
    """Base error yang aman ditampilkan ke user (bahasa bisnis, bukan teknis)."""

    status_code: int = 400
    message: str = "Terjadi kesalahan."

    def __init__(self, message: str | None = None, errors: dict | None = None, *, detail: str | None = None) -> None:
        super().__init__(message or self.message)
        self.message = message or self.message
        self.errors = errors
        self.detail = detail  # detail teknis, hanya untuk logging, tidak ke client


class BusinessError(AppError):
    """Gagal business validation (contoh: stok tidak mencukupi, HPP belum lengkap)."""

    status_code = 400


class UnauthorizedError(AppError):
    status_code = 401
    message = "Autentikasi diperlukan."


class ForbiddenError(AppError):
    status_code = 403
    message = "Anda tidak memiliki akses ke resource ini."


class NotFoundError(AppError):
    status_code = 404
    message = "Resource tidak ditemukan."


class ConflictError(AppError):
    status_code = 409
    message = "Resource sudah ada atau konflik dengan data yang ada."