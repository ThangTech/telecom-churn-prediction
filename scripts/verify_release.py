"""Week 6 release smoke test without evaluating the test partition again."""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import warnings
from importlib.metadata import version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sklearn.exceptions import InconsistentVersionWarning

from app.backend.main import app
from app.backend.service import get_prediction_service
from scripts.verify_week4_thang import verify_week4
from src.features import CONFIRMED_MODEL_FEATURES

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports/week6-thang-release-verification.json"

EXPECTED = {
    "numpy": "2.4.6",
    "pandas": "3.0.6",
    "scikit-learn": "1.9.1",
    "scipy": "1.17.1",
    "joblib": "1.6.0",
    "matplotlib": "3.11.2",
    "seaborn": "0.13.2",
    "fastapi": "0.142.2",
    "httpx": "0.28.1",
    "pydantic": "2.13.5",
    "uvicorn": "0.54.0",
}

SMOKE_FEATURES = {
    "Call  Failure": 1,
    "Complains": 0,
    "Subscription  Length": 24,
    "Charge  Amount": 2,
    "Seconds of Use": 1000,
    "Frequency of use": 80,
    "Frequency of SMS": 12,
    "Distinct Called Numbers": 20,
    "Age Group": 3,
    "Tariff Plan": 1,
    "Status": 1,
    "Age": 35,
    "Customer Value": 42.75,
}


def _command_version(command: list[str]) -> str | None:
    if os.name == "nt" and command[0] == "npm":
        command = ["cmd", "/c", *command]
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def verify_release() -> dict[str, object]:
    installed = {name: version(name) for name in EXPECTED}
    checks: dict[str, bool] = {
        "python_3_11_9": platform.python_version() == "3.11.9",
        "locked_python_packages": installed == EXPECTED,
        "smoke_fixture_has_frozen_features": list(SMOKE_FEATURES) == CONFIRMED_MODEL_FEATURES,
    }

    week4 = verify_week4()
    checks["week4_acceptance_passes"] = week4["status"] == "PASS"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        service = get_prediction_service()
    checks["model_load_has_no_version_warning"] = not any(
        isinstance(item.message, InconsistentVersionWarning) for item in caught
    )

    prediction = service.score(SMOKE_FEATURES, "MEDIUM")
    checks["api_smoke_probability_is_valid"] = (
        0.0 <= float(prediction["churn_probability"]) <= 1.0
        and prediction["capacity_mode"] == "MEDIUM"
        and prediction["threshold"] == service.thresholds["MEDIUM"]
        and prediction["predicted_churn"]
        == (prediction["churn_probability"] >= prediction["threshold"])
    )

    paths = {route.path for route in app.routes}
    checks["openapi_contains_required_endpoints"] = {"/api/health", "/api/churn-score"}.issubset(paths)

    node_version = _command_version(["node", "--version"])
    npm_version = _command_version(["npm", "--version"])
    checks["node_20_or_newer"] = bool(node_version) and int(node_version.lstrip("v").split(".")[0]) >= 20
    checks["npm_available"] = npm_version is not None

    failed = [name for name, passed in checks.items() if not passed]
    return {
        "status": "PASS" if not failed else "FAIL",
        "scope": "Release and inference smoke test only; no test labels were loaded and no evaluation metrics were recomputed.",
        "checks": checks,
        "failed_checks": failed,
        "environment": {
            "python": platform.python_version(),
            "packages": installed,
            "node": node_version,
            "npm": npm_version,
        },
        "model_version": service.model_version,
        "smoke_prediction": prediction,
    }


def main() -> None:
    result = verify_release()
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
