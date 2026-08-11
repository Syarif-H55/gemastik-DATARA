"""Router agregat utama API DATARA.

Struktur canonical (dipasang di prefix ``/api`` oleh ``app.main``):

.. code-block:: text

    /api
    ├── /health         (infrastruktur, liveness)
    ├── /health/db      (infrastruktur, readiness)
    └── /v1             (seluruh business API /api/v1/*)
"""
from fastapi import APIRouter

from app.api.routes import health
from app.api.v1 import v1_router

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(v1_router, prefix="/v1")

__all__ = ["api_router"]