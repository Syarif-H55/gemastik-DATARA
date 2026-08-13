"""Seed data demo untuk 2 pengguna DATARA (development lokal).

Menghasilkan dua profil pengguna yang realistis agar teman yang mengerjakan
frontend langsung punya data untuk dites:

* **Veteran** — sudah memakai aplikasi +/- 6 bulan (180 hari transaksi).
  Bisnis: kedai kopi "Kopi Nusantara", katalog 7 produk, tren penjualan yang
  tumbuh stabil dari +/- 45% -> 110% volume saat ini, biaya operasional
  rutin per bulan, dan target bulanan yang tercapai (COMPLETED/ACTIVE).
* **Pemula** — baru memakai +/- 1 bulan (30 hari transaksi).
  Bisnis: "Warung Makan Bu Sari", katalog 6 produk, volume kecil dan masih
  fluktuatif (awal bulan beberapa hari tidak tercatat), biaya operasional
  1 bulan, target bulanan.

Data dibuat agar "masuk akal":

* HPP per unit = bahan baku + kemasan + tenaga kerja langsung + overhead,
  dengan margin wajar per jenis bisnis.
* Stok menurun oleh transaksi dan di-restock saat berada di bawah ambang
  (movement RESTOCK tercatat, stok tidak pernah negatif).
* Pola mingguan (weekend lebih ramai), noise harian, dan tren pertumbuhan.
* Transaksi dibuat lewat ``transaction_service.create_sale`` sehingga
  stok, movement SALE, dan snapshot HPP konsisten dengan aplikasi.

Contoh:

.. code-block:: bash

    python -m scripts.seed_demo_2users --password rahasia123
"""
import argparse
import random
from datetime import date, datetime, timedelta

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.business_configuration import BusinessConfiguration
from app.models.business_target import BusinessTarget
from app.models.enums import (
    CostType,
    ExpenseType,
    MovementType,
    PeriodType,
    TargetStatus,
    TargetType,
)
from app.models.operating_expense import OperatingExpense
from app.repositories import business_repository, product_repository, user_repository
from app.schemas.transaction import TransactionCreateRequest, TransactionItemRequest
from app.services import transaction_service

# ---------------------------------------------------------------------------
# Profil pengguna
# ---------------------------------------------------------------------------

# (nama, sku, harga jual, unit, ambang stok, qty restock, permintaan dasar/hari)
# HPP = (bahan baku, kemasan, tenaga kerja langsung, overhead)
VETERAN_PRODUCTS = [
    ("Espresso", "MIN-001", 15000, "gelas", 15, 60, 10,
     (2800, 500, 400, 300)),
    ("Kopi Susu Gula Aren", "MIN-002", 20000, "gelas", 20, 120, 22,
     (5000, 1000, 600, 500)),
    ("Kopi Tubruk", "MIN-003", 12000, "gelas", 15, 50, 9,
     (1800, 400, 300, 300)),
    ("Es Teh Manis", "MIN-004", 7000, "gelas", 20, 100, 18,
     (1200, 500, 300, 300)),
    ("Matcha Latte", "MIN-005", 22000, "gelas", 10, 45, 8,
     (6200, 1000, 600, 500)),
    ("Kentang Goreng", "SNK-001", 15000, "porsi", 15, 70, 12,
     (3000, 600, 700, 400)),
    ("Roti Bakar Cokelat", "SNK-002", 12000, "porsi", 15, 60, 10,
     (2600, 700, 500, 400)),
]

NEWCOMER_PRODUCTS = [
    ("Nasi Ayam Geprek", "FOOD-001", 18000, "porsi", 12, 80, 16,
     (6200, 800, 1500, 500)),
    ("Nasi Goreng Ayam", "FOOD-002", 20000, "porsi", 10, 60, 11,
     (6800, 800, 1600, 500)),
    ("Mie Goreng", "FOOD-003", 18000, "porsi", 10, 50, 9,
     (5600, 700, 1400, 450)),
    ("Es Teh Manis", "MIN-001", 5000, "gelas", 20, 80, 14,
     (800, 500, 300, 200)),
    ("Es Jeruk", "MIN-002", 8000, "gelas", 15, 45, 8,
     (2200, 600, 400, 250)),
    ("Kerupuk & Lalapan", "SNK-001", 5000, "porsi", 20, 60, 10,
     (700, 300, 200, 150)),
]

# (expense_type, nama, jumlah, tanggal dalam bulan)
VETERAN_EXPENSES = [
    (ExpenseType.RENT, "Sewa tempat bulanan", 3500000, 1),
    (ExpenseType.FIXED_SALARY, "Gaji 2 karyawan", 4000000, 28),
    (ExpenseType.ADMINISTRATIVE, "Pulsa & administrasi", 300000, 10),
    (ExpenseType.OTHER, "Listrik & air", 600000, 20),
]

NEWCOMER_EXPENSES = [
    (ExpenseType.RENT, "Sewa tempat bulanan", 1200000, 1),
    (ExpenseType.FIXED_SALARY, "Gaji pembantu warung", 1800000, 27),
    (ExpenseType.ADMINISTRATIVE, "Kulakan & administrasi", 150000, 10),
    (ExpenseType.OTHER, "Listrik & air", 350000, 20),
]

VETERAN = {
    "email": "dummy.lama@umkm.id",
    "name": "Dewi Anggraini",
    "business_name": "Kopi Nusantara",
    "safety_days": 4,
    "lead_time": 2,
    "target_margin": 45,
    "days": 180,
    "growth": (0.45, 1.10),
    "noise": (0.72, 1.32),
    "skip_days": 0,
    "skip_prob": 0.0,
    "sale_hours": (7, 13),
    "seed": 20240101,
    "products": VETERAN_PRODUCTS,
    "expenses": VETERAN_EXPENSES,
}

NEWCOMER = {
    "email": "dummy.baru@umkm.id",
    "name": "Sari Wulandari",
    "business_name": "Warung Makan Bu Sari",
    "safety_days": 3,
    "lead_time": 3,
    "target_margin": 35,
    "days": 30,
    "growth": (0.55, 1.05),
    "noise": (0.55, 1.50),
    "skip_days": 8,
    "skip_prob": 0.25,
    "sale_hours": (10, 15),
    "seed": 20240315,
    "products": NEWCOMER_PRODUCTS,
    "expenses": NEWCOMER_EXPENSES,
}

_WEEKDAY_FACTOR = {0: 0.88, 1: 1.00, 2: 1.00, 3: 1.02, 4: 1.12, 5: 1.50, 6: 1.28}

_COST_TYPES = (
    CostType.RAW_MATERIAL,
    CostType.PACKAGING,
    CostType.DIRECT_LABOR,
    CostType.PRODUCTION_OVERHEAD,
)


def _month_range(year: int, month: int) -> tuple[date, date]:
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)
    return start, end


def _round_thousand(value: float) -> int:
    return int(round(value / 1000.0) * 1000)


def _seed_products(db, business_id: int, profile: dict) -> list:
    """Buat produk + komponen HPP + stok awal. Return list (product, metadata)."""
    seeded = []
    for name, sku, price, unit, threshold, restock, daily, hpp in profile["products"]:
        product = product_repository.create(
            db,
            business_id=business_id,
            name=name,
            sku=sku,
            selling_price=price,
            unit=unit,
            low_stock_threshold=threshold,
        )
        for cost_type, amount in zip(_COST_TYPES, hpp):
            product_repository.upsert_cost(
                db,
                product_id=product.id,
                cost_type=cost_type,
                name=cost_type.name.replace("_", " ").title(),
                cost_per_unit=amount,
            )
        product_repository.create_inventory(
            db, business_id=business_id, product_id=product.id, current_stock=restock * 2
        )
        seeded.append((product, daily, restock, threshold))
    db.flush()
    return seeded


def _seed_expenses(db, business_id: int, profile: dict) -> dict:
    """Buat biaya operasional per bulan. Return dict (tahun, bulan) -> total biaya."""
    today = datetime.now().date()
    period_start = today - timedelta(days=profile["days"])
    monthly_total: dict[tuple[int, int], float] = {}

    year, month = period_start.year, period_start.month
    while (year, month) <= (today.year, today.month):
        for expense_type, name, amount, day in profile["expenses"]:
            expense_date = date(year, month, day)
            if expense_date > today:
                continue
            db.add(
                OperatingExpense(
                    business_id=business_id,
                    expense_type=expense_type,
                    name=name,
                    amount=amount,
                    expense_date=expense_date,
                )
            )
            monthly_total[(year, month)] = monthly_total.get((year, month), 0.0) + float(amount)
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    db.flush()
    return monthly_total


def _seed_transactions(db, business, profile: dict) -> tuple[dict, list[int]]:
    """Generate transaksi harian + restock. Return (total bulanan, ids produk)."""
    rng = random.Random(profile["seed"])
    today = datetime.now()
    period_start = today - timedelta(days=profile["days"])

    monthly: dict[tuple[int, int], dict] = {}
    product_ids: list[int] = []
    growth_start, growth_end = profile["growth"]
    span = max(1, profile["days"] - 1)
    low_hour, high_hour = profile["sale_hours"]

    records = 0
    for day_index in range(profile["days"]):
        day = period_start + timedelta(days=day_index)
        growth = growth_start + (growth_end - growth_start) * (day_index / span)
        weekday_factor = _WEEKDAY_FACTOR[day.weekday()]

        for product, daily, restock_qty, threshold in profile["_seeded_products"]:
            base = daily * growth * weekday_factor
            quantity = round(base * rng.uniform(*profile["noise"]))
            if day_index < profile["skip_days"] and rng.random() < profile["skip_prob"]:
                continue
            if quantity < 1:
                continue

            inventory = product_repository.get_inventory_by_product(db, product.id)
            current = float(inventory.current_stock)
            if current - quantity < threshold:
                movement_date = day.replace(hour=8, minute=30)
                new_stock = current + restock_qty
                product_repository.create_movement(
                    db,
                    business_id=business.id,
                    product_id=product.id,
                    movement_type=MovementType.RESTOCK,
                    quantity=restock_qty,
                    movement_date=movement_date,
                    note="Pembelian stok rutin",
                    stock_after=new_stock,
                )
                product_repository.set_stock(db, inventory, new_stock)
                current = new_stock

            payload = TransactionCreateRequest(
                transaction_date=day.replace(
                    hour=rng.randint(low_hour, high_hour), minute=rng.randint(0, 59)
                ),
                customer_name=None,
                discount=0,
                items=[TransactionItemRequest(product_id=product.id, quantity=float(quantity))],
            )
            tx = transaction_service.create_sale(db, business, payload)

            key = (day.year, day.month)
            bucket = monthly.setdefault(key, {"sales": 0.0, "cogs": 0.0})
            bucket["sales"] += float(tx["total"])
            for item in tx["items"]:
                bucket["cogs"] += float(item["unit_hpp"]) * float(item["quantity"])
            product_ids.append(product.id)
            records += 1

    print(f"  transaksi dibuat: {records}")
    return monthly, product_ids


def _seed_targets(db, business_id: int, monthly: dict, expense_total: dict, today: date) -> None:
    for (year, month), actual in sorted(monthly.items()):
        is_current = (year, month) == (today.year, today.month)
        status = TargetStatus.ACTIVE if is_current else TargetStatus.COMPLETED
        start_date, end_date = _month_range(year, month)
        expenses = expense_total.get((year, month), 0.0)
        net_profit = actual["sales"] - actual["cogs"] - expenses

        sales_target = _round_thousand(actual["sales"] * (1.15 if is_current else 1.03))
        profit_target = _round_thousand(max(0.0, net_profit) * (1.15 if is_current else 1.03))
        db.add(
            BusinessTarget(
                business_id=business_id,
                target_type=TargetType.SALES,
                target_value=sales_target,
                period_type=PeriodType.MONTHLY,
                start_date=start_date,
                end_date=end_date,
                status=status,
            )
        )
        db.add(
            BusinessTarget(
                business_id=business_id,
                target_type=TargetType.PROFIT,
                target_value=profit_target,
                period_type=PeriodType.MONTHLY,
                start_date=start_date,
                end_date=end_date,
                status=status,
            )
        )
    db.flush()


def _seed_user(db, profile: dict, password: str) -> int | None:
    existing = user_repository.get_by_email(db, profile["email"])
    if existing is not None:
        print(f"User {profile['email']} sudah ada. Skip (hapus manual untuk seed ulang).")
        return None

    print(f"Seeding {profile['name']} ({profile['business_name']}) ...")
    user = user_repository.create(
        db,
        name=profile["name"],
        email=profile["email"],
        password_hash=hash_password(password),
    )
    business = business_repository.create(
        db,
        user_id=user.id,
        name=profile["business_name"],
        business_type="food_beverage",
    )
    db.add(
        BusinessConfiguration(
            business_id=business.id,
            safety_days=profile["safety_days"],
            lead_time=profile["lead_time"],
            target_margin=profile["target_margin"],
        )
    )
    profile["_seeded_products"] = _seed_products(db, business.id, profile)
    expense_total = _seed_expenses(db, business.id, profile)
    db.commit()

    monthly, _product_ids = _seed_transactions(db, business, profile)
    _seed_targets(db, business.id, monthly, expense_total, datetime.now().date())
    db.commit()
    return user.id


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed data demo 2 pengguna DATARA")
    parser.add_argument("--password", required=True, help="Password bersama untuk 2 akun demo")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        for profile in (VETERAN, NEWCOMER):
            user_id = _seed_user(db, profile, args.password)
            if user_id is not None:
                print(f"  user id={user_id} email={profile['email']}")
        print("Selesai.")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())