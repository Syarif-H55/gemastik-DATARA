"""Skema untuk endpoint health check."""
from pydantic import BaseModel


class HealthData(BaseModel):
    status: str
    app: str
    version: str


class HealthDbData(BaseModel):
    status: str
    database: str