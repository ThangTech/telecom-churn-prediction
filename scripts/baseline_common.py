"""Frozen split and shared utilities for Thang's independent scripts."""
import json
from pathlib import Path

import pandas as pd
import sklearn

from src.data import (ROW_ID_COLUMN, assert_split_integrity, basic_cleaning,
                      build_train_validation_split, compare_columns_against_dictionary,
                      compute_checksum, load_raw_data)
from src.features import CONFIRMED_MODEL_FEATURES, PENDING_VERIFICATION_FEATURES

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/Customer Churn.csv"
MANIFEST = ROOT / "data/processed/split_indices.json"
SEED = 42


def prepare_data():
    raw = load_raw_data(RAW)
    compare_columns_against_dictionary(raw, ROOT / "data/data_dictionary.csv")
    data = basic_cleaning(raw)
    checksum = compute_checksum(RAW, "sha256")
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if manifest["raw_sha256"] != checksum or manifest["seed"] != SEED:
            raise ValueError("Frozen split does not match raw data/seed. Investigate before replacing it.")
        by_id = data.set_index(ROW_ID_COLUMN, drop=False)
        splits = tuple(by_id.loc[manifest["row_ids"][name]].reset_index(drop=True) for name in ["train", "validation", "test"])
    else:
        splits = build_train_validation_split(data, random_state=SEED)
        manifest = {
            "raw_path": "data/raw/Customer Churn.csv", "raw_sha256": checksum, "seed": SEED,
            "split_method": "StratifiedGroupKFold 5 folds; full-row content groups; 3/1/1 folds",
            "sklearn_version": sklearn.__version__,
            "row_ids": {name: part[ROW_ID_COLUMN].tolist() for name, part in zip(["train", "validation", "test"], splits)},
        }
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    assert_split_integrity(data, *splits)
    keys = [set(pd.util.hash_pandas_object(part.drop(columns=ROW_ID_COLUMN), index=False)) for part in splits]
    if any(keys[i] & keys[j] for i, j in [(0, 1), (0, 2), (1, 2)]):
        raise ValueError("Duplicate content crosses frozen split boundaries.")
    return splits, manifest


def model_inputs(frame):
    return frame[CONFIRMED_MODEL_FEATURES].copy(), frame["Churn"].copy()


def write_config(path, extra):
    import platform
    import numpy
    payload = {
        "status": "provisional_metadata_pending", "seed": SEED,
        "features": CONFIRMED_MODEL_FEATURES, "excluded_pending": PENDING_VERIFICATION_FEATURES,
        "excluded_technical": ["row_id", "Churn"], "classification_threshold": 0.5,
        "precision_zero_division": 0, "PR_summary": "Average Precision (not trapezoidal PR-AUC)",
        "python": platform.python_version(), "pandas": pd.__version__,
        "numpy": numpy.__version__, "sklearn": sklearn.__version__, **extra,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
