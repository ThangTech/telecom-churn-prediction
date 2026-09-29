from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

TARGET_COLUMN = "Churn"

# Iranian Churn Dataset expected columns
# Note: Some column names contain extra whitespace in the raw CSV
DEFAULT_EXPECTED_COLUMNS = [
    "Call  Failure",           # Note: 2 spaces between "Call" and "Failure"
    "Complains",
    "Subscription  Length",    # Note: 2 spaces between "Subscription" and "Length"
    "Charge  Amount",          # Note: 2 spaces between "Charge" and "Amount"
    "Seconds of Use",
    "Frequency of use",
    "Frequency of SMS",
    "Distinct Called Numbers",
    "Age Group",
    "Tariff Plan",
    "Status",
    "Age",
    "Customer Value",
    TARGET_COLUMN,
]

# Column name normalization mapping (original → normalized)
# Preserves original names but documents whitespace anomalies
COLUMN_NAME_MAPPING = {
    "Call  Failure": "Call  Failure",              # Preserved as-is
    "Subscription  Length": "Subscription  Length", # Preserved as-is
    "Charge  Amount": "Charge  Amount",            # Preserved as-is
}


def load_raw_data(path: str | Path) -> pd.DataFrame:
    """Đọc file CSV dữ liệu thô."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại: {file_path}")

    df = pd.read_csv(file_path)
    df.columns = [str(col).strip() for col in df.columns]
    return df


def load_dictionary_columns(path: str | Path) -> list[str]:
    """Đọc danh sách cột từ data_dictionary.csv nếu có."""
    file_path = Path(path)
    if not file_path.exists():
        return []

    dictionary = pd.read_csv(file_path)
    if "field_name" not in dictionary.columns:
        return []

    return [str(col).strip() for col in dictionary["field_name"].dropna().tolist()]


def compare_columns(df: pd.DataFrame, expected_columns: list[str] | None = None) -> dict[str, list[str]]:
    """So sánh tên cột thực tế với schema dự kiến."""
    target_columns = expected_columns or DEFAULT_EXPECTED_COLUMNS
    actual = list(df.columns)

    missing = [col for col in target_columns if col not in actual]
    extra = [col for col in actual if col not in target_columns]
    unexpected_order = [
        actual[idx]
        for idx in range(min(len(actual), len(target_columns)))
        if actual[idx] != target_columns[idx]
    ]

    return {
        "expected": target_columns,
        "actual": actual,
        "missing": missing,
        "extra": extra,
        "unexpected_order": unexpected_order,
    }


def compare_columns_against_dictionary(df: pd.DataFrame, dictionary_path: str | Path) -> dict[str, list[str]]:
    """So sánh schema dữ liệu với file mô tả cột."""
    dictionary_columns = load_dictionary_columns(dictionary_path)
    if not dictionary_columns:
        return compare_columns(df)
    return compare_columns(df, dictionary_columns)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names by stripping leading/trailing whitespace only.
    
    Note: Does NOT modify internal whitespace (e.g., 'Call  Failure' stays as-is).
    This preserves the original structure from the raw CSV file.
    """
    normalized = df.copy()
    normalized.columns = [str(col).strip() for col in normalized.columns]
    return normalized


def validate_schema(
    df: pd.DataFrame,
    expected_columns: list[str] | None = None,
    strict: bool = False
) -> dict[str, Any]:
    """Validate dataset schema against expected columns.
    
    Args:
        df: DataFrame to validate
        expected_columns: List of expected column names (uses DEFAULT_EXPECTED_COLUMNS if None)
        strict: If True, raises ValueError on schema mismatch
    
    Returns:
        Dictionary with validation results: missing, extra, valid
    """
    expected = expected_columns or DEFAULT_EXPECTED_COLUMNS
    actual = list(df.columns)
    
    missing = [col for col in expected if col not in actual]
    extra = [col for col in actual if col not in expected]
    valid = len(missing) == 0 and len(extra) == 0
    
    result = {
        "valid": valid,
        "expected_count": len(expected),
        "actual_count": len(actual),
        "missing": missing,
        "extra": extra,
    }
    
    if strict and not valid:
        raise ValueError(
            f"Schema validation failed:\n"
            f"  Missing columns: {missing}\n"
            f"  Extra columns: {extra}"
        )
    
    return result


def check_missing(df: pd.DataFrame) -> dict[str, int]:
    """Check for missing values in all columns."""
    missing = df.isnull().sum()
    return {col: count for col, count in missing.items() if count > 0}


def check_duplicates(df: pd.DataFrame) -> dict[str, Any]:
    """Check for duplicate rows."""
    n_duplicates = df.duplicated().sum()
    return {
        "n_duplicates": int(n_duplicates),
        "percentage": float(n_duplicates / len(df) * 100) if len(df) > 0 else 0.0,
    }


def check_invalid_values(df: pd.DataFrame) -> dict[str, Any]:
    """Check for invalid values in specific columns (Iranian dataset rules)."""
    issues = {}
    
    # Check Churn target (must be 0 or 1)
    if TARGET_COLUMN in df.columns:
        invalid_churn = df[~df[TARGET_COLUMN].isin([0, 1])]
        if len(invalid_churn) > 0:
            issues[TARGET_COLUMN] = {
                "invalid_count": len(invalid_churn),
                "invalid_values": invalid_churn[TARGET_COLUMN].unique().tolist(),
            }
    
    # Check numeric columns for negative values where inappropriate
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        if col in ["Age", "Subscription  Length", "Frequency of use", "Frequency of SMS"]:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                if col not in issues:
                    issues[col] = {}
                issues[col]["negative_count"] = int(negative_count)
    
    return issues


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """Perform basic deterministic data cleaning for Iranian Churn Dataset.
    
    This function performs ONLY deterministic, lossless transformations:
    - Strip column whitespace (leading/trailing only)
    - Remove exact duplicate rows
    - Ensure target column has correct dtype
    
    NOTE: NO imputation, NO scaling, NO encoding - those are done post-split.
    """
    cleaned = df.copy()
    
    # Normalize column names (strip only)
    cleaned.columns = [str(col).strip() for col in cleaned.columns]
    
    # Remove exact duplicates
    n_before = len(cleaned)
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    n_after = len(cleaned)
    if n_before != n_after:
        print(f"Removed {n_before - n_after} duplicate rows")
    
    # Ensure target is numeric (0/1)
    if TARGET_COLUMN in cleaned.columns:
        # Iranian dataset already has 0/1, just ensure dtype
        cleaned[TARGET_COLUMN] = pd.to_numeric(cleaned[TARGET_COLUMN], errors="coerce")
        
        if cleaned[TARGET_COLUMN].isnull().any():
            raise ValueError(f"Target column '{TARGET_COLUMN}' contains non-numeric values")
        
        # Validate binary values
        unique_vals = cleaned[TARGET_COLUMN].unique()
        if not set(unique_vals).issubset({0, 1, 0.0, 1.0}):
            raise ValueError(
                f"Target column '{TARGET_COLUMN}' must be binary (0/1), "
                f"found: {unique_vals}"
            )
        
        cleaned[TARGET_COLUMN] = cleaned[TARGET_COLUMN].astype(int)
    
    return cleaned


def split_features_target(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN
) -> tuple[pd.DataFrame, pd.Series]:
    """Split DataFrame into features (X) and target (y)."""
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' not found in DataFrame")
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    return X, y


def build_train_validation_split(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN,
    test_size: float = 0.2,
    val_size: float = 0.25,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Chia dữ liệu thành train / validation / test với stratify theo target.
    
    Target split: ~60% train, ~20% validation, ~20% test
    
    Implementation:
    - First split: 80% temp (train+val), 20% test
    - Second split: 75% train, 25% val (of the 80%)
    - Final: 60% train, 20% val, 20% test
    """
    if target_col not in df.columns:
        raise KeyError(f"Không tìm thấy cột nhãn {target_col!r} trong DataFrame.")

    from sklearn.model_selection import train_test_split

    # First split: 80% temp, 20% test
    temp_df, test_df = train_test_split(
        df,
        test_size=test_size,
        stratify=df[target_col],
        random_state=random_state,
    )
    
    # Second split: 75% train, 25% val (of the 80% = 60% and 20% of total)
    train_df, val_df = train_test_split(
        temp_df,
        test_size=val_size,
        stratify=temp_df[target_col],
        random_state=random_state,
    )

    return train_df.reset_index(drop=True), val_df.reset_index(drop=True), test_df.reset_index(drop=True)


def summarize_dataset(df: pd.DataFrame) -> dict[str, Any]:
    """Tạo tóm tắt nhanh về số dòng, cột, missing và nhãn."""
    summary = {
        "shape": df.shape,
        "missing_values": df.isna().sum().sort_values(ascending=False).to_dict(),
        "target_distribution": (
            df[TARGET_COLUMN].value_counts(normalize=True).sort_index().round(4).to_dict()
            if TARGET_COLUMN in df.columns
            else {}
        ),
    }
    return summary
