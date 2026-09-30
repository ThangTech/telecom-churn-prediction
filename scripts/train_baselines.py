"""Week 2: B0 constant probability and B1 unweighted logistic; validation only."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import joblib
import numpy as np
import pandas as pd

from scripts.baseline_common import ROOT, model_inputs, prepare_data, write_config
from src.baseline_pipeline import make_pipeline
from src.metrics import evaluate_probabilities


def main():
    (train, validation, _), manifest = prepare_data()
    X_train, y_train = model_inputs(train)
    X_val, y_val = model_inputs(validation)
    rate = float(y_train.mean())
    p0 = np.full(len(y_val), rate)
    pipeline = make_pipeline()
    pipeline.fit(X_train, y_train)
    p1 = pipeline.predict_proba(X_val)[:, 1]
    results = pd.DataFrame([
        {"model": "B0_constant_train_rate", **evaluate_probabilities(y_val, p0)},
        {"model": "B1_logistic_unweighted", **evaluate_probabilities(y_val, p1)},
    ])
    (ROOT / "models").mkdir(exist_ok=True)
    joblib.dump(pipeline, ROOT / "models/b1_pipeline.joblib")
    results.to_csv(ROOT / "reports/validation_baselines.csv", index=False)
    write_config(ROOT / "configs/baselines.json", {
        "raw_sha256": manifest["raw_sha256"], "B0_train_churn_rate": rate,
        "B1": {"C": 1.0, "class_weight": None}, "evaluation_partition": "validation",
        "test_evaluated": False,
    })
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
