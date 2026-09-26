from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split

from data import (
    TARGET_COLUMN,
    build_train_validation_split,
    clean_telco_data,
    compare_columns_against_dictionary,
    load_raw_data,
    summarize_dataset,
)


def run_eda(train_df: pd.DataFrame, output_dir: str | Path = "reports/figures") -> dict:
    """Thực hiện EDA cơ bản trên tập train, lưu các hình ảnh và thống kê mô tả."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    summary = summarize_dataset(train_df)

    # Save text summary
    summary_df = pd.DataFrame(
        {
            "metric": ["n_rows", "n_columns", "target_rate_0", "target_rate_1"],
            "value": [
                train_df.shape[0],
                train_df.shape[1],
                summary["target_distribution"].get(0, 0.0),
                summary["target_distribution"].get(1, 0.0),
            ],
        }
    )
    summary_df.to_csv(output_path / "train_summary.csv", index=False)

    # Plot 1: target distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(data=train_df, x=TARGET_COLUMN, palette="Set2")
    plt.title("Target distribution on train")
    plt.xlabel("Churn")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(output_path / "target_distribution.png", dpi=200)
    plt.close()

    # Plot 2: missing values
    missing = train_df.isna().sum().sort_values(ascending=False)
    if not missing.empty and missing.sum() > 0:
        plt.figure(figsize=(10, 5))
        missing[missing > 0].plot(kind="bar", color="steelblue")
        plt.title("Missing values by column")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(output_path / "missing_values.png", dpi=200)
        plt.close()

    # Plot 3: numeric distributions
    numeric_cols = train_df.select_dtypes(include=["number"]).columns.tolist()
    if "customerID" in numeric_cols:
        numeric_cols.remove("customerID")
    if numeric_cols:
        fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(10, 3 * max(len(numeric_cols), 1)))
        for ax, col in zip(axes, numeric_cols):
            sns.histplot(train_df[col], bins=30, kde=True, ax=ax)
            ax.set_title(f"Distribution of {col}")
        fig.tight_layout()
        fig.savefig(output_path / "numeric_distributions.png", dpi=200)
        plt.close(fig)

    # Plot 4: churn rate by key categorical columns
    cat_cols = [
        col
        for col in train_df.columns
        if col not in {TARGET_COLUMN, "customerID"} and train_df[col].dtype == "object"
    ]
    if cat_cols:
        fig, axes = plt.subplots(min(len(cat_cols), 4), 1, figsize=(10, 4 * min(len(cat_cols), 4)))
        for ax, col in zip(axes, cat_cols[: min(len(cat_cols), 4)]):
            churn_rate = (
                train_df.groupby(col)[TARGET_COLUMN]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
            )
            sns.barplot(data=churn_rate, x=col, y=TARGET_COLUMN, ax=ax, palette="viridis")
            ax.set_title(f"Churn rate by {col}")
            ax.set_ylabel("Churn rate")
            ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        fig.savefig(output_path / "churn_rate_by_category.png", dpi=200)
        plt.close(fig)

    return summary


def main() -> None:
    raw_path = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    dictionary_path = "data/data_dictionary.csv"

    raw_df = load_raw_data(raw_path)
    schema_check = compare_columns_against_dictionary(raw_df, dictionary_path)
    print("Schema check:")
    for key in ["missing", "extra", "unexpected_order"]:
        if schema_check[key]:
            print(f"- {key}: {schema_check[key]}")
        else:
            print(f"- {key}: none")

    cleaned_df = clean_telco_data(raw_df)
    train_df, valid_df, test_df = build_train_validation_split(cleaned_df, target_col=TARGET_COLUMN)

    print("\nTrain shape:", train_df.shape)
    print("Validation shape:", valid_df.shape)
    print("Test shape:", test_df.shape)
    print("Train target distribution:", train_df[TARGET_COLUMN].value_counts(normalize=True).to_dict())

    eda_summary = run_eda(train_df, output_dir="reports/figures")
    print("\nEDA completed.")
    print("Summary:", eda_summary)


if __name__ == "__main__":
    main()
