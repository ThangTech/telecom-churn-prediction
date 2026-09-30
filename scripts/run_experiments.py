"""Week 3: grouped CV on train; compare weights; choose by mean CV AP."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import StratifiedGroupKFold

from scripts.baseline_common import ROOT, SEED, model_inputs, prepare_data, write_config
from src.baseline_pipeline import make_pipeline
from src.metrics import evaluate_probabilities


def main():
    (train, validation, _), manifest = prepare_data()
    X, y = model_inputs(train)
    X_val, y_val = model_inputs(validation)
    groups = pd.util.hash_pandas_object(train.drop(columns="row_id"), index=False).astype(str)
    folds = list(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED).split(X, y, groups))
    records = []
    summaries = []
    for weight in [None, "balanced"]:
        for C in [0.1, 1.0, 10.0]:
            run = f"{'B1' if weight is None else 'M1'}_C{C:g}"
            scores = []
            for fold, (fit_idx, heldout_idx) in enumerate(folds):
                if set(groups.iloc[fit_idx]) & set(groups.iloc[heldout_idx]):
                    raise ValueError("Duplicate content crosses CV fold boundary.")
                model = make_pipeline(class_weight=weight, C=C)
                model.fit(X.iloc[fit_idx], y.iloc[fit_idx])
                metrics = evaluate_probabilities(y.iloc[heldout_idx], model.predict_proba(X.iloc[heldout_idx])[:, 1])
                records.append({"run": run, "class_weight": weight or "none", "C": C, "fold": fold, **metrics})
                scores.append(metrics)
            summaries.append({
                "run": run, "class_weight": weight or "none", "C": C,
                **{metric + suffix: float(op([s[metric] for s in scores]))
                   for metric in ["AP", "ROC_AUC", "Brier", "precision", "recall", "F1"]
                   for suffix, op in [("_mean", np.mean), ("_std", lambda a: np.std(a, ddof=1))]},
            })
    summary = pd.DataFrame(summaries)
    # Stable tie handling: the declared configuration order wins equal mean AP.
    chosen = summaries[int(np.argmax(summary["AP_mean"].values))]
    chosen_weight = None if chosen["class_weight"] == "none" else "balanced"
    val_records = []
    probabilities = {}
    for name, weight, C in [("B1_C1", None, 1.0), ("M1_C1", "balanced", 1.0),
                            ("candidate_selected_by_train_CV", chosen_weight, chosen["C"])]:
        model = make_pipeline(class_weight=weight, C=C)
        model.fit(X, y)
        p = model.predict_proba(X_val)[:, 1]
        probabilities[name] = p
        val_records.append({"model": name, "class_weight": weight or "none", "C": C, **evaluate_probabilities(y_val, p)})
        if name == "candidate_selected_by_train_CV":
            joblib.dump(model, ROOT / "models/week3_candidate.joblib")
    pd.DataFrame(records).to_csv(ROOT / "reports/week3_cv_folds.csv", index=False)
    summary.to_csv(ROOT / "reports/week3_experiments.csv", index=False)
    pd.DataFrame(val_records).to_csv(ROOT / "reports/week3_validation.csv", index=False)
    fig_dir = ROOT / "reports/figures/thang"
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot([0, 1], [0, 1], "--", color="gray", label="Ideal")
    bins = []
    for name, p in probabilities.items():
        actual, predicted = calibration_curve(y_val, p, n_bins=10, strategy="uniform")
        ax.plot(predicted, actual, marker="o", label=name)
        bucket = np.minimum((p * 10).astype(int), 9)
        for b in range(10):
            mask = bucket == b
            bins.append({"model": name, "bin": b, "count": int(mask.sum()),
                         "mean_probability": float(p[mask].mean()) if mask.any() else None,
                         "observed_churn_rate": float(y_val.to_numpy()[mask].mean()) if mask.any() else None})
    ax.set(xlabel="Mean predicted probability", ylabel="Observed churn rate", title="Validation calibration (provisional)")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(fig_dir / "validation_calibration.png", dpi=160); plt.close(fig)
    pd.DataFrame(bins).to_csv(ROOT / "reports/week3_calibration_bins.csv", index=False)
    p = probabilities["candidate_selected_by_train_CV"]
    ConfusionMatrixDisplay.from_predictions(y_val, (p >= 0.5).astype(int), labels=[0, 1])
    plt.title("Candidate validation confusion matrix (threshold 0.5)")
    plt.tight_layout(); plt.savefig(fig_dir / "validation_confusion_matrix.png", dpi=160); plt.close()
    write_config(ROOT / "configs/experiments.json", {
        "raw_sha256": manifest["raw_sha256"], "CV": "5-fold StratifiedGroupKFold on train only",
        "search_C": [0.1, 1.0, 10.0], "search_class_weight": [None, "balanced"],
        "selection_metric": "highest mean train-CV AP; configuration order breaks ties",
        "selected": chosen, "test_evaluated": False,
    })
    print(summary[["run", "AP_mean", "AP_std", "ROC_AUC_mean", "Brier_mean"]].to_string(index=False))
    print("Selected from train CV:", chosen["run"])
    print(pd.DataFrame(val_records).to_string(index=False))


if __name__ == "__main__":
    main()
