"""Week 4 analysis helpers with validation-only threshold selection."""
from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from src.metrics import evaluate_probabilities


def threshold_for_capacity(probability: Iterable[float], capacity: float) -> tuple[float, int]:
    """Return the probability cut-off selecting approximately the top capacity share."""
    values = np.asarray(list(probability), dtype=float)
    if values.size == 0 or not np.isfinite(values).all() or ((values < 0) | (values > 1)).any():
        raise ValueError("Probabilities must be a non-empty finite array in [0,1].")
    if not 0 < capacity <= 1:
        raise ValueError("Capacity must be in (0,1].")
    count = max(1, int(np.ceil(capacity * len(values))))
    descending = np.sort(values)[::-1]
    if count == len(values):
        threshold = 0.0
    elif descending[count - 1] == descending[count]:
        threshold = float(descending[count - 1])
    else:
        threshold = float((descending[count - 1] + descending[count]) / 2)
    return threshold, count


def evaluate_capacity_thresholds(y_true, probability, capacities=(0.10, 0.20, 0.30)) -> pd.DataFrame:
    records = []
    for label, capacity in zip(("LOW", "MEDIUM", "HIGH"), capacities, strict=True):
        threshold, intended_count = threshold_for_capacity(probability, capacity)
        metrics = evaluate_probabilities(y_true, probability, threshold=threshold)
        records.append(
            {
                "capacity_level": label,
                "capacity_rate": float(capacity),
                "threshold": threshold,
                "intended_capacity_count": intended_count,
                "coverage_rate": metrics["predicted_positive"] / metrics["n_samples"],
                **metrics,
            }
        )
    return pd.DataFrame(records)


def fit_tertile_edges(values: Iterable[float]) -> list[float]:
    """Fit low/medium/high cut points from predictors only, never from target."""
    series = pd.Series(values, dtype=float)
    if series.empty or not np.isfinite(series).all():
        raise ValueError("Grouping values must be non-empty and finite.")
    q1, q2 = series.quantile([1 / 3, 2 / 3]).tolist()
    if q1 == q2:
        raise ValueError("Tertile boundaries collapse to one value.")
    return [float("-inf"), float(q1), float(q2), float("inf")]


def assign_tertiles(values: Iterable[float], edges: Iterable[float]) -> pd.Categorical:
    return pd.cut(values, bins=list(edges), labels=["low", "medium", "high"], include_lowest=True)


def grouped_error_metrics(
    frame: pd.DataFrame,
    target,
    prediction,
    feature: str,
    edges: Iterable[float],
) -> pd.DataFrame:
    """Report error metrics for predictor-defined groups."""
    working = pd.DataFrame(
        {
            "group": assign_tertiles(frame[feature], edges),
            "target": np.asarray(target, dtype=int),
            "prediction": np.asarray(prediction, dtype=int),
        }
    )
    records = []
    for group in ["low", "medium", "high"]:
        part = working.loc[working["group"] == group]
        y = part["target"].to_numpy()
        pred = part["prediction"].to_numpy()
        tp = int(((y == 1) & (pred == 1)).sum())
        fp = int(((y == 0) & (pred == 1)).sum())
        fn = int(((y == 1) & (pred == 0)).sum())
        tn = int(((y == 0) & (pred == 0)).sum())
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        records.append(
            {
                "group": group,
                "lower_bound": list(edges)[["low", "medium", "high"].index(group)],
                "upper_bound": list(edges)[["low", "medium", "high"].index(group) + 1],
                "n_samples": len(part),
                "churn_rate": float(y.mean()) if len(y) else np.nan,
                "precision": precision,
                "recall": recall,
                "F1": f1,
                "TN": tn,
                "FP": fp,
                "FN": fn,
                "TP": tp,
            }
        )
    return pd.DataFrame(records)


def extract_logistic_coefficients(pipeline) -> pd.DataFrame:
    preprocessing = pipeline.named_steps["preprocessing"]
    model = pipeline.named_steps["model"]
    names = preprocessing.get_feature_names_out()
    coefficients = np.asarray(model.coef_).reshape(-1)
    if len(names) != len(coefficients):
        raise ValueError("Transformed feature names do not match coefficient count.")
    cleaned = [name.split("__", 1)[-1] for name in names]
    result = pd.DataFrame({"feature": cleaned, "coefficient": coefficients})
    result["abs_coefficient"] = result["coefficient"].abs()
    result["direction"] = np.where(result["coefficient"] > 0, "positive", np.where(result["coefficient"] < 0, "negative", "zero"))
    return result.sort_values("abs_coefficient", ascending=False, ignore_index=True)
