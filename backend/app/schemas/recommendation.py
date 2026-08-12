"""Skema request/response untuk Smart Pricing & Smart Restock (API Contract bab 13-14)."""
from pydantic import BaseModel, Field


class PricingRecommendationCreateRequest(BaseModel):
    product_id: int
    target_margin: float = Field(default=30, ge=0, le=100)


class PricingApplyRequest(BaseModel):
    recommendation_id: int


class PricingDismissRequest(BaseModel):
    recommendation_id: int


class RestockRecommendationCreateRequest(BaseModel):
    product_id: int


class RestockApplyRequest(BaseModel):
    recommendation_id: int


class RestockDismissRequest(BaseModel):
    recommendation_id: int
