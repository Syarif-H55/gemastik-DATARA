"""Registrasi exception handler FastAPI agar semua error terstruktur.

Body error konsisten dengan API Contract DATARA:

.. code-block:: json

    {"success": false, "message": "...", "errors": {...}}
"""
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError

logger = logging.getLogger("datara.api")


def _error_response(status_code: int, message: str, errors: dict | None = None) -> JSONResponse:
    body: dict = {"success": False, "message": message}
    if errors:
        body["errors"] = errors
    return JSONResponse(status_code=status_code, content=body)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        if exc.detail:
            logger.warning("AppError %s: %s", exc.status_code, exc.detail)
        return _error_response(exc.status_code, exc.message, exc.errors)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors: dict[str, list[str]] = {}
        for err in exc.errors():
            field = ".".join(str(part) for part in err.get("loc", []) if part != "body")
            errors.setdefault(field, []).append(err.get("msg", "Invalid value"))
        return _error_response(422, "Data tidak valid.", errors)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        detail = exc.detail
        if isinstance(detail, dict):
            detail = detail.get("message", "Request gagal.")
        return _error_response(exc.status_code, str(detail))

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return _error_response(500, "Terjadi kesalahan internal. Silakan coba lagi.")