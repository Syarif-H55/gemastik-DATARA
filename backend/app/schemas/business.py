"""Skema request/response untuk Business API (API Contract bab 5)."""
from pydantic import BaseModel, Field


class BusinessUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    business_type: str | None = Field(default=None, max_length=100)
    safety_days: float | None = Field(default=None, ge=0)
