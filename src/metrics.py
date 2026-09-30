"""Validation metrics shared by B0, B1 and Week 3 experiments."""
import numpy as np
from sklearn.metrics import (
    average_precision_score, brier_score_loss, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score,
)


def evaluate_probabilities(y, probability, threshold=0.5):
    p = np.asarray(probability, dtype=float)
    if len(y) != len(p) or not np.isfinite(p).all() or ((p < 0) | (p > 1)).any():
        raise ValueError("Probabilities must be finite, in [0,1], and match target length.")
    prediction = (p >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()
    return {
        "threshold": threshold, "n_samples": len(y), "AP": average_precision_score(y, p),
        "ROC_AUC": roc_auc_score(y, p), "Brier": brier_score_loss(y, p),
        "precision": precision_score(y, prediction, zero_division=0),
        "recall": recall_score(y, prediction, zero_division=0),
        "F1": f1_score(y, prediction, zero_division=0),
        "predicted_positive": int(prediction.sum()),
        "precision_defined": bool(prediction.sum()),
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
    }
