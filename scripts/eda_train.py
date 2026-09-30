"""Canonical Week 2 EDA. All analytical statistics come from train only."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

from src.data import (  # noqa: E402
    ROW_ID_COLUMN,
    TARGET_COLUMN,
    basic_cleaning,
    build_train_validation_split,
    check_duplicates,
    load_raw_data,
)

FIGURES = ROOT / "reports" / "figures"
REPORT = ROOT / "reports" / "eda_results_week2.md"
KEY_FEATURES = ["Subscription  Length", "Charge  Amount", "Complains"]
PENDING_FEATURES = ["Status", "Customer Value"]


def _save_target(train: pd.DataFrame) -> str:
    counts = train[TARGET_COLUMN].value_counts().sort_index()
    ax = counts.plot.bar(color=["#4c78a8", "#f58518"], title="Target distribution — train only")
    ax.set(xlabel="Churn", ylabel="Count")
    plt.tight_layout()
    plt.savefig(FIGURES / "target_distribution.png", dpi=160)
    plt.close()
    return f"Train churn rate is {train[TARGET_COLUMN].mean():.2%}; the classes are imbalanced."


def _save_key_features(train: pd.DataFrame) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for axis, column in zip(axes, KEY_FEATURES):
        sns.histplot(data=train, x=column, hue=TARGET_COLUMN, element="step", stat="density", common_norm=False, ax=axis)
        axis.set_title(column)
    fig.suptitle("Required feature distributions — train only")
    fig.tight_layout()
    fig.savefig(FIGURES / "key_feature_distributions.png", dpi=160)
    plt.close(fig)
    return "The three required variables have different ranges and non-Gaussian shapes; scaling should be fitted inside the training pipeline."


def _save_correlation(train: pd.DataFrame) -> str:
    numeric = train.drop(columns=[ROW_ID_COLUMN]).select_dtypes(include="number")
    corr = numeric.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, cmap="coolwarm", center=0, square=False)
    plt.title("Correlation heatmap — train only")
    plt.tight_layout()
    plt.savefig(FIGURES / "correlation_matrix.png", dpi=160)
    plt.close()
    return "The heatmap identifies linear associations worth checking for redundancy; it does not establish causation or leakage."


def _save_pending(train: pd.DataFrame) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.countplot(data=train, x="Status", hue=TARGET_COLUMN, ax=axes[0])
    axes[0].set_title("Status — descriptive only")
    sns.histplot(data=train, x="Customer Value", hue=TARGET_COLUMN, element="step", ax=axes[1])
    axes[1].set_title("Customer Value — descriptive only")
    fig.tight_layout()
    fig.savefig(FIGURES / "pending_features_descriptive.png", dpi=160)
    plt.close(fig)
    return "Both variables show statistical patterns, but their definitions and availability before prediction remain unverified."


def run_eda() -> dict:
    FIGURES.mkdir(parents=True, exist_ok=True)
    raw = load_raw_data(ROOT / "data" / "raw" / "Customer Churn.csv")
    cleaned = basic_cleaning(raw)
    train, _, _ = build_train_validation_split(cleaned)

    missing = train.isna().sum()
    duplicates = check_duplicates(train)
    descriptive = "```text\n" + train[KEY_FEATURES].describe().round(3).to_string() + "\n```"
    target_counts = train[TARGET_COLUMN].value_counts().sort_index()
    target_table = "| Churn | count |\n|---:|---:|\n" + "\n".join(
        f"| {label} | {count} |" for label, count in target_counts.items()
    )
    findings = {
        "target": _save_target(train),
        "key": _save_key_features(train),
        "correlation": _save_correlation(train),
        "pending": _save_pending(train),
    }

    report = f"""# Week 2 EDA Results — Train Only

Canonical command: `python scripts/eda_train.py`.

## Scope guard

- Analytical input: train split only ({len(train):,} rows).
- Validation and test are not inspected for distributions, correlations, feature selection, preprocessing, thresholds, or class weights.
- No preprocessing transformer is fitted by this script.

## Data checks

- Missing values in train: {int(missing.sum())}
- Excess duplicate-content rows within train: {duplicates['n_duplicate_excess_rows']}
- Duplicate contents were retained. The grouped splitter prevents identical content crossing split boundaries.

## Target distribution

{target_table}

**Purpose:** quantify class balance on train before modeling.

**Finding:** {findings['target']}

**Limitation:** this is one split and contains no performance evidence.

**Allowed conclusion:** use stratification and compare `class_weight=None` with `class_weight="balanced"` using validation only.

## Descriptive statistics

{descriptive}

## Required feature distributions

Artifact: `reports/figures/key_feature_distributions.png`

**Purpose:** inspect scale, skew and class-conditional distributions for Subscription Length, Charge Amount and Complains.

**Finding:** {findings['key']}

**Limitation:** visual differences are associations, not causal effects. IQR/extreme values are not automatically errors.

**Allowed conclusion:** use a train-fitted scaler inside the Logistic Regression pipeline; do not delete rows solely from these plots.

## Correlation heatmap

Artifact: `reports/figures/correlation_matrix.png`

**Purpose:** summarize pairwise linear association on train.

**Finding:** {findings['correlation']}

**Limitation:** correlation misses nonlinear relationships and cannot determine feature availability at prediction time.

**Allowed conclusion:** use it as descriptive evidence only, never as a leakage rule.

## Pending-verification features

Artifact: `reports/figures/pending_features_descriptive.png`

**Purpose:** document train-only distributions without making an eligibility decision.

**Finding:** {findings['pending']}

**Limitation:** repository metadata does not define how or when either variable is produced.

**Allowed conclusion:** `Status` and `Customer Value` remain excluded from the default model feature set until authoritative temporal evidence is recorded.

## Artifacts

- `reports/figures/target_distribution.png`
- `reports/figures/key_feature_distributions.png`
- `reports/figures/correlation_matrix.png`
- `reports/figures/pending_features_descriptive.png`
"""
    REPORT.write_text(report, encoding="utf-8")
    return {"train_rows": len(train), "missing": int(missing.sum()), "duplicates": duplicates}


if __name__ == "__main__":
    print(run_eda())
    print(f"Wrote {REPORT.relative_to(ROOT)}")
