"""Seed data demo DATARA: user, business, produk, HPP, stok, biaya, transaksi.

Menghasilkan data realistis dari transaksi aktual agar dashboard, forecasting,
pricing, restock, dan growth langsung dapat dilihat setelah login.

Contoh:

.. code-block:: bash

    python -m scripts.seed_demo_data \
        --email owner@umkm.id --name "Budi" --password "rahasia123" \
        --business "Kedai Contoh"
"""
import argparse
import random
from datetime import datetime, timedelta

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.business import Business
from app.models.business_configuration import BusinessConfiguration
from app.models.enums import CostType, ExpenseType
from app.models.operating_expense import OperatingExpense
from app.repositories import business_repository, product_repository, user_repository
from app.schemas.transaction import TransactionCreateRequest, TransactionItemRequest
from app.services import transaction_service

# (nama, sku, harga jual, unit, ambang stok, stok awal, rata-rata terjual/hari)
PRODUCTS = [
    ("Es Teh Manis", "MIN-001", 5000, "gelas", 10, 220, 15),
    ("Es Jeruk Peras", "MIN-002", 8000, "gelas", 10, 100, 7),
    ("Kopi Susu Gula Aren", "MIN-003", 15000, "gelas", 10, 200, 12),
    ("Ayam Geprek + Nasi", "FOOD-001", 18000, "porsi", 15, 210, 14),
    ("Nasi Goreng Spesial", "FOOD-002", 20000, "porsi", 15, 150, 9),
    ("Kentang Goreng", "SNK-001", 12000, "porsi", 20, 130, 8),
    ("Pisang Goreng Keju", "SNK-002", 10000, "porsi", 15, 148, 10),
    ("Air Mineral 600ml", "MIN-004", 4000, "botol", 24, 250, 15),
]

# Komponen HPP per produk: (raw_material, packaging, direct_labor, overhead)
COSTS = [
    (1000, 300, 100, 100),
    (2300, 500, 200, 200),
    (5200, 1000, 400, 300),
    (7500, 1500, 1000, 500),
    (8800, 1600, 1000, 400),
    (3400, 900, 600, 300),
    (2900, 800, 500, 200),
    (1900, 300, 200, 100),
]

DAYS = 14


def _seed_products(db, business_id: int) -> list[int]:
    product_ids: list[int] = []
    for (name, sku, price, unit, threshold, initial_stock, _daily), costs in zip(PRODUCTS, COSTS):
        product = product_repository.create(
            db,
            business_id=business_id,
            name=name,
            sku=sku,
            selling_price=price,
            unit=unit,
            low_stock_threshold=threshold,
        )
        for cost_type, amount in zip(
            [CostType.RAW_MATERIAL, CostType.PACKAGING, CostType.DIRECT_LABOR, CostType.PRODUCTION_OVERHEAD],
            costs,
        ):
            product_repository.upsert_cost(
                db,
                product_id=product.id,
                cost_type=cost_type,
                name=cost_type.name.replace("_", " ").title(),
                cost_per_unit=amount,
            )
        product_repository.create_inventory(
            db, business_id=business_id, product_id=product.id, current_stock=initial_stock
        )
        product_ids.append(product.id)
    db.flush()
    return product_ids


def _seed_expenses(db, business_id: int) -> None:
    today = datetime.now().date()
    expenses = [
        (ExpenseType.RENT, "Sewa tempat bulanan", 1500000, today - timedelta(days=28)),
        (ExpenseType.FIXED_SALARY, "Gaji tetap karyawan", 3000000, today - timedelta(days=15)),
        (ExpenseType.ADMINISTRATIVE, "Pulsa & administrasi", 300000, today - timedelta(days=6)),
    ]
    for expense_type, name, amount, expense_date in expenses:
        db.add(
            OperatingExpense(
                business_id=business_id,
                expense_type=expense_type,
                name=name,
                amount=amount,
                expense_date=expense_date,
            )
        )
    db.flush()


def _seed_transactions(db, business: Business, product_specs: list) -> None:
    rng = random.Random(42)
    today = datetime.now()
    for day_offset in range(DAYS, 0, -1):
        day = today - timedelta(days=day_offset)
        for (name, _sku, _price, _unit, _thr, _stock, daily), product_id in zip(PRODUCTS, product_specs):
            qty = max(1, daily + rng.randint(-3, 3))
            payload = TransactionCreateRequest(
                transaction_date=day.replace(hour=10 + rng.randint(0, 9), minute=rng.randint(0, 59)),
                customer_name=None,
                discount=0,
                items=[TransactionItemRequest(product_id=product_id, quantity=float(qty))],
            )
            transaction_service.create_sale(db, business, payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed data demo DATARA")
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--business", required=True)
    parser.add_argument("--business-type", default="food_beverage")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        existing = user_repository.get_by_email(db, args.email)
        if existing is not None:
            print(f"User {args.email} sudah ada. Untuk seed ulang, hapus user tersebut dulu.")
            return 0

        user = user_repository.create(
            db,
            name=args.name,
            email=args.email,
            password_hash=hash_password(args.password),
        )
        business = business_repository.create(
            db,
            user_id=user.id,
            name=args.business,
            business_type=args.business_type,
        )
        db.add(BusinessConfiguration(business_id=business.id, safety_days=3, lead_time=3, target_margin=30))
        db.flush()

        product_ids = _seed_products(db, business.id)
        _seed_expenses(db, business.id)
        db.commit()
        print(f"Seeded user id={user.id}, business id={business.id}, {len(product_ids)} produk.")

        # Transaksi dibuat setelah produk & stok awal tersedia (mengurangi stok secara nyata).
        _seed_transactions(db, business, product_ids)
        db.commit()
        print("Seeded transaksi penjualan 14 hari terakhir.")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
