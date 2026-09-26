from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

TARGET_COLUMN = "Churn"
DEFAULT_EXPECTED_COLUMNS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    TARGET_COLUMN,
]


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


def clean_telco_data(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch và chuẩn hóa dữ liệu khách hàng viễn thông."""
    cleaned = df.copy()
    cleaned.columns = cleaned.columns.str.strip()
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    for col in cleaned.columns:
        if cleaned[col].dtype == object:
            cleaned[col] = cleaned[col].astype(str).str.strip()
            cleaned[col] = cleaned[col].replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})

    if "customerID" in cleaned.columns:
        cleaned["customerID"] = cleaned["customerID"].astype(str)

    if "TotalCharges" in cleaned.columns:
        cleaned["TotalCharges"] = pd.to_numeric(cleaned["TotalCharges"], errors="coerce")

    for numeric_col in ["tenure", "MonthlyCharges", "TotalCharges"]:
        if numeric_col in cleaned.columns:
            cleaned[numeric_col] = pd.to_numeric(cleaned[numeric_col], errors="coerce")
            median_value = cleaned[numeric_col].median()
            if pd.notna(median_value):
                cleaned[numeric_col] = cleaned[numeric_col].fillna(median_value)

    object_columns = cleaned.select_dtypes(include=["object"]).columns.tolist()
    for col in object_columns:
        if col == TARGET_COLUMN:
            continue
        mode_value = cleaned[col].mode(dropna=True)
        if not mode_value.empty:
            cleaned[col] = cleaned[col].fillna(mode_value.iloc[0])

    if TARGET_COLUMN in cleaned.columns:
        cleaned[TARGET_COLUMN] = cleaned[TARGET_COLUMN].astype(str).str.strip().str.lower()
        cleaned[TARGET_COLUMN] = cleaned[TARGET_COLUMN].map({"yes": 1, "no": 0, "true": 1, "false": 0})
        if cleaned[TARGET_COLUMN].isna().any():
            unexpected = sorted(cleaned.loc[cleaned[TARGET_COLUMN].isna(), TARGET_COLUMN].unique().tolist())
            raise ValueError(f"Giá trị nhãn không hợp lệ trong {TARGET_COLUMN}: {unexpected}")

    return cleaned


def build_train_validation_split(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN,
    test_size: float = 0.2,
    val_size: float = 0.25,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Chia dữ liệu thành train / validation / test với stratify theo target."""
    if target_col not in df.columns:
        raise KeyError(f"Không tìm thấy cột nhãn {target_col!r} trong DataFrame.")

    from sklearn.model_selection import train_test_split

    train_df, temp_df = train_test_split(
        df,
        test_size=test_size,
        stratify=df[target_col],
        random_state=random_state,
    )
    val_df, test_df = train_test_split(
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
