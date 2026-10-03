"""Public request and response schemas for the churn API."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class ChurnScoreRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    features: dict[str, Any]
    capacity_mode: Literal["LOW", "MEDIUM", "HIGH"]


class ChurnScoreResponse(BaseModel):
    churn_probability: float
    predicted_churn: bool
    priority_group: Literal["HIGH", "MEDIUM", "EXTENDED", "NOT_PRIORITIZED"]
    threshold: float
    capacity_mode: Literal["LOW", "MEDIUM", "HIGH"]
    model_version: str
    request_id: str


class HealthResponse(BaseModel):
    status: Literal["ok"]
    model_version: str
    feature_count: int
