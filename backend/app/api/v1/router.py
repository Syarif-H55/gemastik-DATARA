"""Router API bisnis versi 1 (canonical: ``/api/v1``).

Seluruh rute bisnis (auth, businesses, products, transactions, inventory,
finance, dashboard, forecasting, pricing, restock, decisions, growth,
assistant) ditambahkan ke ``v1_router`` di sini, sesuai API Contract DATARA.

``v1_router`` dipasang pada prefix ``/v1`` di dalam ``api_router`` sehingga
hasil akhir berada di ``/api/v1``. Endpoint health tidak pindah — tetap di
``/api/health`` dan ``/api/health/db``.

Contoh:

.. code-block:: python

    from app.api.v1.routes import products
    v1_router.include_router(products.router, prefix="/products", tags=["products"])
"""
from fastapi import APIRouter

from app.api.v1.routes import (
    assistant,
    auth,
    business,
    business_health,
    dashboard,
    decisions,
    finance,
    forecasting,
    growth,
    inventory,
    pricing,
    products,
    restock,
    transactions,
)

v1_router = APIRouter()
v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
v1_router.include_router(business.router, prefix="/business", tags=["business"])
v1_router.include_router(products.router, prefix="/products", tags=["products"])
v1_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
v1_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
v1_router.include_router(finance.router, prefix="/finance", tags=["finance"])
v1_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
v1_router.include_router(forecasting.router, prefix="/forecasting", tags=["forecasting"])
v1_router.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
v1_router.include_router(restock.router, prefix="/restock", tags=["restock"])
v1_router.include_router(business_health.router, prefix="/health", tags=["health"])
v1_router.include_router(decisions.router, prefix="/decisions", tags=["decisions"])
v1_router.include_router(growth.router, prefix="/growth", tags=["growth"])
v1_router.include_router(assistant.router, prefix="/ai", tags=["assistant"])
