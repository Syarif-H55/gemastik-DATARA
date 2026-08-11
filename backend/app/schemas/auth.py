"""Skema request/response untuk Authentication API (API Contract bab 4)."""
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=6, max_length=128)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str


class BusinessResponse(BaseModel):
    id: int
    name: str
    business_type: str
    safety_days: float
