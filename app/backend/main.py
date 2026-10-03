"""FastAPI entry point for the Week 5 churn prediction service."""
from __future__ import annotations

import os
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.backend.schemas import ChurnScoreRequest, ChurnScoreResponse, HealthResponse
from app.backend.service import InputValidationError, get_prediction_service
from src.features import CONFIRMED_MODEL_FEATURES


def _allowed_origins() -> list[str]:
    configured = os.getenv(
        "CHURN_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    return [item.strip() for item in configured.split(",") if item.strip()]


app = FastAPI(
    title="Telecom Churn Prediction API",
    version="1.0.0",
    description="Loads the frozen Week 4 pipeline and returns churn probabilities.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.exception_handler(InputValidationError)
async def input_validation_handler(_request: Request, exc: InputValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"code": "INVALID_FEATURE_VALUE", "message": str(exc), "details": exc.details},
    )


@app.exception_handler(RequestValidationError)
async def request_validation_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    details = [
        {"field": ".".join(str(part) for part in item["loc"] if part != "body"), "message": item["msg"]}
        for item in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"code": "INVALID_REQUEST", "message": "Request validation failed", "details": details},
    )


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    service = get_prediction_service()
    return HealthResponse(status="ok", model_version=service.model_version, feature_count=len(CONFIRMED_MODEL_FEATURES))


@app.post("/api/churn-score", response_model=ChurnScoreResponse)
def churn_score(payload: ChurnScoreRequest) -> ChurnScoreResponse:
    service = get_prediction_service()
    result = service.score(payload.features, payload.capacity_mode)
    return ChurnScoreResponse(**result, request_id=str(uuid.uuid4()))
