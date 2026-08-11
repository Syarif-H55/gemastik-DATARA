"""Skema request/response untuk Inventory API (API Contract bab 9)."""
from datetime import datetime

from pydantic import BaseModel, Field


class InventoryMovementCreateRequest(BaseModel):
    product_id: int
    movement_type: str = Field(pattern="^(received|waste|adjustment)$")
    # Untuk received/waste harus > 0; untuk adjustment boleh negatif/positif
    # (nilai bertanda: + menambah stok, - mengurangi stok).
    quantity: float
    movement_date: datetime | None = None
    note: str | None = Field(default=None, max_length=255)
