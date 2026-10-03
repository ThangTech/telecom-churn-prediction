"""Prediction service backed by the frozen Week 4 sklearn pipeline."""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import joblib
import pandas as pd

from src.features import CONFIRMED_MODEL_FEATURES

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models/week4_final_candidate.joblib"
CONFIG_PATH = ROOT / "configs/week4_frozen_evaluation.json"

CapacityMode = Literal["LOW", "MEDIUM", "HIGH"]

INTEGER_FEATURES = {
    "Call  Failure",
    "Complains",
    "Subscription  Length",
    "Charge  Amount",
    "Seconds of Use",
    "Frequency of use",
    "Frequency of SMS",
    "Distinct Called Numbers",
    "Age Group",
    "Tariff Plan",
    "Status",
    "Age",
}
ALLOWED_VALUES = {
    "Complains": {0, 1},
    "Charge  Amount": set(range(10)),
    "Age Group": set(range(1, 6)),
    "Tariff Plan": {1, 2},
    "Status": {1, 2},
}


class InputValidationError(ValueError):
    def __init__(self, details: list[dict[str, str]]):
        super().__init__("Input validation failed")
        self.details = details


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_features(features: dict[str, Any]) -> dict[str, int | float]:
    expected = set(CONFIRMED_MODEL_FEATURES)
    supplied = set(features)
    details: list[dict[str, str]] = []
    for name in sorted(expected - supplied):
        details.append({"field": name, "message": "field is required"})
    for name in sorted(supplied - expected):
        details.append({"field": name, "message": "unexpected field"})
    if details:
        raise InputValidationError(details)

    cleaned: dict[str, int | float] = {}
    for name in CONFIRMED_MODEL_FEATURES:
        value = features[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            details.append({"field": name, "message": "must be a number"})
            continue
        numeric = float(value)
        if not math.isfinite(numeric):
            details.append({"field": name, "message": "must be finite"})
            continue
        if numeric < 0:
            details.append({"field": name, "message": "must be greater than or equal to 0"})
            continue
        if name in INTEGER_FEATURES and not numeric.is_integer():
            details.append({"field": name, "message": "must be an integer"})
            continue
        integer_value = int(numeric)
        if name in ALLOWED_VALUES and integer_value not in ALLOWED_VALUES[name]:
            allowed = sorted(ALLOWED_VALUES[name])
            details.append({"field": name, "message": f"must be one of {allowed}"})
            continue
        cleaned[name] = integer_value if name in INTEGER_FEATURES else numeric

    if details:
        raise InputValidationError(details)
    return cleaned


@dataclass(frozen=True)
class ChurnPredictionService:
    pipeline: Any
    thresholds: dict[str, float]
    model_version: str

    @classmethod
    def load(cls) -> "ChurnPredictionService":
        if not MODEL_PATH.exists() or not CONFIG_PATH.exists():
            raise FileNotFoundError("Frozen Week 4 model or config is missing.")
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        if config.get("status") != "final_test_evaluated":
            raise RuntimeError("Week 4 configuration is not in the frozen final state.")
        thresholds = {
            row["capacity_level"]: float(row["threshold"])
            for row in config["capacity_thresholds"]
        }
        if set(thresholds) != {"LOW", "MEDIUM", "HIGH"}:
            raise RuntimeError("Frozen config must define LOW, MEDIUM and HIGH thresholds.")

        pipeline = joblib.load(MODEL_PATH)
        model_features = list(pipeline.named_steps["preprocessing"].feature_names_in_)
        if model_features != CONFIRMED_MODEL_FEATURES or model_features != config["features"]:
            raise RuntimeError("Model, source feature list and frozen config do not match.")
        model_version = f"week4-final-{_sha256(MODEL_PATH)[:12]}"
        return cls(pipeline=pipeline, thresholds=thresholds, model_version=model_version)

    def priority_group(self, probability: float) -> str:
        if probability >= self.thresholds["LOW"]:
            return "HIGH"
        if probability >= self.thresholds["MEDIUM"]:
            return "MEDIUM"
        if probability >= self.thresholds["HIGH"]:
            return "EXTENDED"
        return "NOT_PRIORITIZED"

    def score(self, features: dict[str, Any], capacity_mode: CapacityMode) -> dict[str, object]:
        cleaned = validate_features(features)
        frame = pd.DataFrame([cleaned], columns=CONFIRMED_MODEL_FEATURES)
        probability = float(self.pipeline.predict_proba(frame)[0, 1])
        if not math.isfinite(probability) or not 0.0 <= probability <= 1.0:
            raise RuntimeError("Model returned an invalid probability.")
        threshold = self.thresholds[capacity_mode]
        return {
            "churn_probability": probability,
            "predicted_churn": probability >= threshold,
            "priority_group": self.priority_group(probability),
            "threshold": threshold,
            "capacity_mode": capacity_mode,
            "model_version": self.model_version,
        }


@lru_cache(maxsize=1)
def get_prediction_service() -> ChurnPredictionService:
    return ChurnPredictionService.load()
