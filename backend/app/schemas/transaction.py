"""Skema request/response untuk Sales Transaction API (API Contract bab 8)."""
from datetime import datetime

from pydantic import BaseModel, Field


class TransactionItemRequest(BaseModel):
    product_id: int
    quantity: float = Field(gt=0)
    selling_price: float | None = Field(default=None, ge=0)


class TransactionCreateRequest(BaseModel):
    transaction_date: datetime | None = None
    customer_name: str | None = Field(default=None, max_length=150)
    discount: float = Field(default=0, ge=0)
    items: list[TransactionItemRequest] = Field(min_length=1)
