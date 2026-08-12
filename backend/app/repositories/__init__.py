"""Lapisan repositories untuk akses data per entitas.

Repository membungkus query SQLAlchemy agar service tetap fokus pada
business logic dan tidak menulis query berulang.
"""
from app.repositories import (  # noqa: F401
    business_configuration_repository,
    business_repository,
    expense_repository,
    product_repository,
    recommendation_repository,
    transaction_repository,
    user_repository,
)
