"""Week 4 acceptance audit without reopening the test labels.

This script verifies the frozen configuration, model structure, thresholds and
published confusion-matrix arithmetic.  It deliberately does not load the raw
test target or call ``predict_proba`` on the test split.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import joblib
import pandas as pd

from src.baseline_pipeline import CATEGORICAL, NUMERIC
from src.features import CONFIRMED_MODEL_FEATURES

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs/week4_frozen_evaluation.json"
MODEL_PATH = ROOT / "models/week4_final_candidate.joblib"
FINAL_REPORT_PATH = ROOT / "reports/week4_test_final.csv"
VALIDATION_THRESHOLDS_PATH = ROOT / "reports/week4_thresholds_validation.csv"
TEST_THRESHOLDS_PATH = ROOT / "reports/week4_test_thresholds.csv"
FRONTEND_CONFIG_PATH = ROOT / "web/src/config/model.ts"
OUTPUT_PATH = ROOT / "reports/week4-thang-verification.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _close(actual: float, expected: float, tolerance: float = 1e-12) -> bool:
    return math.isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=tolerance)


def _frontend_thresholds() -> dict[str, float]:
    source = FRONTEND_CONFIG_PATH.read_text(encoding="utf-8")
    matches = re.findall(r"^\s*(LOW|MEDIUM|HIGH):\s*([0-9.]+),", source, flags=re.MULTILINE)
    if len(matches) != 3:
        raise AssertionError("Could not read all three frozen thresholds from frontend config.")
    return {name: float(value) for name, value in matches}


def verify_week4() -> dict[str, object]:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    checks["frozen_status"] = (
        config["status"] == "final_test_evaluated"
        and config["test_evaluation_count"] == 1
        and config["test_evaluated"] is True
        and config["test_used_for_tuning"] is False
        and config["test_decisions_changed_after_evaluation"] is False
    )
    checks["selection_did_not_use_test"] = (
        "validation" in config["threshold_source"].lower()
        and "test" not in config["threshold_source"].lower()
        and config["selection_source"].startswith("train-only")
    )

    raw_path = ROOT / config["raw_file"]
    manifest_path = ROOT / config["split_manifest"]
    checks["raw_checksum"] = sha256(raw_path) == config["raw_sha256"]
    checks["split_manifest_checksum"] = sha256(manifest_path) == config["split_manifest_sha256"]

    model = joblib.load(MODEL_PATH)
    preprocessing = model.named_steps["preprocessing"]
    classifier = model.named_steps["model"]
    transformer_columns = {
        name: list(columns)
        for name, _transformer, columns in preprocessing.transformers
        if name in {"numeric", "categorical"}
    }
    checks["model_feature_order"] = list(preprocessing.feature_names_in_) == CONFIRMED_MODEL_FEATURES
    checks["model_configuration"] = (
        float(classifier.C) == float(config["model"]["C"])
        and classifier.class_weight == config["model"]["class_weight"]
        and int(classifier.random_state) == int(config["model"]["random_state"])
    )
    checks["preprocessing_matches_frozen_config"] = (
        transformer_columns["numeric"] == config["preprocessing"]["numeric_features"] == NUMERIC
        and transformer_columns["categorical"] == config["preprocessing"]["categorical_features"] == CATEGORICAL
    )

    frozen = {row["capacity_level"]: float(row["threshold"]) for row in config["capacity_thresholds"]}
    validation = pd.read_csv(VALIDATION_THRESHOLDS_PATH)
    test_thresholds = pd.read_csv(TEST_THRESHOLDS_PATH)
    validation_values = dict(zip(validation["capacity_level"], validation["threshold"]))
    test_values = dict(zip(test_thresholds["capacity_level"], test_thresholds["frozen_threshold"]))
    frontend_values = _frontend_thresholds()
    checks["thresholds_match_all_consumers"] = all(
        _close(value, validation_values[name])
        and _close(value, test_values[name])
        and _close(value, frontend_values[name])
        for name, value in frozen.items()
    )

    final = pd.read_csv(FINAL_REPORT_PATH).iloc[0]
    tn, fp, fn, tp = (int(final[name]) for name in ("TN", "FP", "FN", "TP"))
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    checks["published_counts_are_complete"] = (
        tn + fp + fn + tp == int(final["n_samples"]) == config["split_sizes"]["test"]
        and tp + fp == int(final["predicted_positive"])
    )
    checks["published_metrics_match_counts"] = (
        _close(final["precision"], precision)
        and _close(final["recall"], recall)
        and _close(final["F1"], f1)
        and _close(final["threshold"], config["primary_threshold"]["threshold"])
    )
    checks["published_probability_metrics_bounded"] = all(
        math.isfinite(float(final[name])) and 0.0 <= float(final[name]) <= 1.0
        for name in ("AP", "PR_AUC", "ROC_AUC", "Brier")
    )

    failed = [name for name, passed in checks.items() if not passed]
    result: dict[str, object] = {
        "status": "PASS" if not failed else "FAIL",
        "scope": "Artifact acceptance only; raw test labels were not loaded and test predictions were not rerun.",
        "checks": checks,
        "failed_checks": failed,
        "artifacts": {
            "frozen_config_sha256": sha256(CONFIG_PATH),
            "model_sha256": sha256(MODEL_PATH),
            "test_report_sha256": sha256(FINAL_REPORT_PATH),
        },
        "published_test_summary": {
            name: (int(final[name]) if name in {"n_samples", "TN", "FP", "FN", "TP"} else float(final[name]))
            for name in ("n_samples", "AP", "PR_AUC", "ROC_AUC", "Brier", "precision", "recall", "F1", "TN", "FP", "FN", "TP")
        },
    }
    return result


def main() -> None:
    result = verify_week4()
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
