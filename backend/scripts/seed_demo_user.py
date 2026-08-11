"""Seed user demo + business untuk development lokal.

API Contract MVP tidak mendefinisikan endpoint ``register``, sehingga akun
awal dibuat lewat script ini (data bisa di-cleanup manual).

Contoh:

.. code-block:: bash

    python -m scripts.seed_demo_user \
        --email owner@umkm.id --name "Budi" --password "rahasia123" \
        --business "Kedai Contoh" --business-type food_beverage
"""
import argparse

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.repositories import business_repository, user_repository


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed user demo DATARA")
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--business", required=True, help="Nama business")
    parser.add_argument("--business-type", default="food_beverage")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        if user_repository.get_by_email(db, args.email):
            print(f"User {args.email} sudah ada. Skip.")
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
        db.commit()
        print(f"Seeded user id={user.id} email={user.email} business id={business.id}")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
