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

v1_router = APIRouter()