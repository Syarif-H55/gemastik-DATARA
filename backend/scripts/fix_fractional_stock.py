"""Perbaiki stok pecahan yang tersimpan karena bug Smart Restock.

Bug lama (sebelum fix): ``suggested_quantity`` direkomendasikan dengan 1 angka
desimal (mis. 12.2) lalu ditambahkan langsung ke stok, sehingga
``inventory_items.current_stock`` menjadi pecahan (mis. 112.2). Stok adalah
satuan unit yang diskrit dan harus bilangan bulat.

Script ini membulatkan data lama ke bilangan bulat terdekat (ROUND):
* ``inventory_items.current_stock`` yang pecahan.
* ``inventory_movements.stock_after`` yang pecahan (riwayat konsisten dengan stok).

Idempotent: baris yang sudah bulat tidak disentuh (hanya yang nilai aslinya
berubah yang di-commit). Tidak mengubah schema.

Contoh:

.. code-block:: bash

    python -m scripts.fix_fractional_stock
"""
from app.db.session import SessionLocal
from app.models.inventory_item import InventoryItem
from app.models.inventory_movement import InventoryMovement


def main() -> int:
    db = SessionLocal()
    rounded = 0
    try:
        rows = (
            db.query(InventoryItem)
            .filter(InventoryItem.current_stock != InventoryItem.current_stock // 1)
            .all()
        )
        for item in rows:
            old = float(item.current_stock)
            new = round(old)
            if new != old:
                item.current_stock = new
                rounded += 1
                print(f"  inventory #{item.product_id}: stok {old:g} -> {new}")

        movements = (
            db.query(InventoryMovement)
            .filter(
                InventoryMovement.stock_after.isnot(None),
                InventoryMovement.stock_after != InventoryMovement.stock_after // 1,
            )
            .all()
        )
        for mv in movements:
            old = float(mv.stock_after)
            new = round(old)
            if new != old:
                mv.stock_after = new
                rounded += 1
                print(f"  movement #{mv.id}: stock_after {old:g} -> {new}")

        db.commit()
        print(f"Selesai. {rounded} baris dibulatkan.")
        return 0
    except Exception as exc:  # pragma: no cover
        db.rollback()
        print(f"Gagal: {exc}")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())