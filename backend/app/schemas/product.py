"""Skema request/response untuk Product & Cost API (API Contract bab 6-7)."""
from pydantic import BaseModel, Field


class ProductCostItemRequest(BaseModel):
    """Satu baris rincian HPP, misal: cup, teh, gula, es batu."""

    name: str = Field(min_length=1, max_length=150)
    cost_per_unit: float = Field(ge=0)


class ProductCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    sku: str | None = Field(default=None, max_length=50)
    selling_price: float = Field(ge=0)
    unit: str = Field(default="unit", max_length=30)
    current_stock: float = Field(default=0, ge=0)
    low_stock_threshold: float | None = Field(default=None, ge=0)
    hpp: float | None = Field(default=None, ge=0)
    cost_items: list[ProductCostItemRequest] | None = Field(default=None)


class ProductUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    sku: str | None = Field(default=None, max_length=50)
    selling_price: float | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, max_length=30)
    low_stock_threshold: float | None = Field(default=None, ge=0)
    is_active: bool | None = None
    cost_items: list[ProductCostItemRequest] | None = Field(default=None)


class ProductCostsUpdateRequest(BaseModel):
    """Ganti total rincian HPP produk (replace-all)."""

    items: list[ProductCostItemRequest]
