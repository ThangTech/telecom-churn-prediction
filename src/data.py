from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from pandas.api.types import is_integer_dtype, is_numeric_dtype, is_object_dtype, is_string_dtype

TARGET_COLUMN = "Churn"
ROW_ID_COLUMN = "row_id"
RANDOM_STATE = 42

DICTIONARY_REQUIRED_FIELDS = {"column_name", "data_type", "description", "role"}
VALID_ROLES = {"feature", "target"}
VALID_DATA_TYPES = {"integer", "float", "numeric", "string", "category", "boolean"}


def compute_checksum(path: str | Path, algorithm: str = "md5") -> str:
    """Return a checksum for the exact file bytes at *path*."""
    digest = hashlib.new(algorithm)
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_raw_data(path: str | Path) -> pd.DataFrame:
    """Read the raw CSV and immediately attach a stable source-row identity."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại: {file_path}")
    df = pd.read_csv(file_path)
    df.columns = [str(column).strip() for column in df.columns]
    if ROW_ID_COLUMN in df.columns:
        raise ValueError(f"Raw data must not already contain technical column {ROW_ID_COLUMN!r}.")
    df.insert(0, ROW_ID_COLUMN, np.arange(len(df), dtype="int64"))
    return df


def load_data_dictionary(path: str | Path) -> pd.DataFrame:
    """Load and validate the dictionary; malformed dictionaries never fall back silently."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy data dictionary tại: {file_path}")
    dictionary = pd.read_csv(file_path)
    missing_fields = sorted(DICTIONARY_REQUIRED_FIELDS - set(dictionary.columns))
    if missing_fields:
        raise ValueError(f"Data dictionary missing required fields: {missing_fields}")
    empty_required = {
        field: int(dictionary[field].isna().sum())
        for field in DICTIONARY_REQUIRED_FIELDS
        if dictionary[field].isna().any()
    }
    if empty_required:
        raise ValueError(f"Data dictionary contains empty required values: {empty_required}")
    dictionary = dictionary.copy()
    dictionary["column_name"] = dictionary["column_name"].astype(str).str.strip()
    if dictionary["column_name"].eq("").any():
        raise ValueError("Data dictionary contains an empty column_name.")
    duplicates = dictionary.loc[dictionary["column_name"].duplicated(keep=False), "column_name"].unique().tolist()
    if duplicates:
        raise ValueError(f"Duplicate column_name entries in data dictionary: {duplicates}")
    invalid_roles = sorted(set(dictionary["role"].dropna()) - VALID_ROLES)
    if invalid_roles:
        raise ValueError(f"Invalid data dictionary roles: {invalid_roles}")
    targets = dictionary.loc[dictionary["role"] == "target", "column_name"].tolist()
    if targets != [TARGET_COLUMN]:
        raise ValueError(f"Data dictionary must define exactly one target named {TARGET_COLUMN!r}; found {targets}.")
    normalized_types = dictionary["data_type"].astype(str).str.lower()
    invalid_types = sorted(set(normalized_types) - VALID_DATA_TYPES)
    if invalid_types:
        raise ValueError(f"Unsupported data_type values in data dictionary: {invalid_types}")
    dictionary["data_type"] = normalized_types
    return dictionary


def load_dictionary_columns(path: str | Path) -> list[str]:
    return load_data_dictionary(path)["column_name"].tolist()


def _dtype_matches(series: pd.Series, declared_type: str) -> bool:
    if declared_type == "integer":
        return is_integer_dtype(series.dtype)
    if declared_type in {"float", "numeric"}:
        return is_numeric_dtype(series.dtype)
    if declared_type in {"string", "category"}:
        return is_string_dtype(series.dtype) or is_object_dtype(series.dtype) or is_integer_dtype(series.dtype)
    if declared_type == "boolean":
        return pd.api.types.is_bool_dtype(series.dtype)
    return False


def validate_schema(
    df: pd.DataFrame,
    dictionary: pd.DataFrame | None = None,
    expected_columns: list[str] | None = None,
    strict: bool = True,
) -> dict[str, Any]:
    """Validate columns and declared dtypes against a validated dictionary/schema."""
    if dictionary is not None:
        expected = dictionary["column_name"].tolist()
    elif expected_columns is not None:
        expected = expected_columns
    else:
        raise ValueError("validate_schema requires a validated dictionary or explicit expected_columns.")
    actual = [column for column in df.columns if column != ROW_ID_COLUMN]
    missing = [column for column in expected if column not in actual]
    extra = [column for column in actual if column not in expected]
    dtype_mismatches: list[dict[str, str]] = []
    if dictionary is not None:
        for record in dictionary[["column_name", "data_type"]].to_dict("records"):
            column = record["column_name"]
            if column in df.columns and not _dtype_matches(df[column], record["data_type"]):
                dtype_mismatches.append({"column": column, "expected": record["data_type"], "actual": str(df[column].dtype)})
    valid = not missing and not extra and not dtype_mismatches
    result = {"valid": valid, "expected": expected, "actual": actual, "missing": missing, "extra": extra, "dtype_mismatches": dtype_mismatches}
    if strict and not valid:
        raise ValueError(f"Schema validation failed: missing={missing}, extra={extra}, dtype_mismatches={dtype_mismatches}")
    return result


def compare_columns(df: pd.DataFrame, expected_columns: list[str]) -> dict[str, Any]:
    return validate_schema(df, expected_columns=expected_columns, strict=False)


def compare_columns_against_dictionary(df: pd.DataFrame, dictionary_path: str | Path) -> dict[str, Any]:
    return validate_schema(df, dictionary=load_data_dictionary(dictionary_path), strict=True)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized.columns = [str(column).strip() for column in normalized.columns]
    return normalized


def check_missing(df: pd.DataFrame) -> dict[str, int]:
    missing = df.isnull().sum()
    return {column: int(count) for column, count in missing.items() if count > 0}


def check_duplicates(df: pd.DataFrame) -> dict[str, Any]:
    """Report duplicate content while ignoring the unique technical row_id."""
    content = df.drop(columns=[ROW_ID_COLUMN], errors="ignore")
    duplicate_mask = content.duplicated(keep="first")
    group_sizes = content.groupby(list(content.columns), dropna=False).size()
    duplicate_groups = group_sizes[group_sizes > 1]
    return {
        "n_duplicate_excess_rows": int(duplicate_mask.sum()),
        "n_duplicate_groups": int(len(duplicate_groups)),
        "n_unique_content_rows": int(len(content.drop_duplicates())),
        "max_group_size": int(duplicate_groups.max()) if len(duplicate_groups) else 1,
        "percentage": float(duplicate_mask.mean() * 100) if len(content) else 0.0,
    }


def check_invalid_values(df: pd.DataFrame) -> dict[str, Any]:
    issues: dict[str, Any] = {}
    if TARGET_COLUMN in df.columns:
        invalid = df.loc[~df[TARGET_COLUMN].isin([0, 1]), TARGET_COLUMN]
        if not invalid.empty:
            issues[TARGET_COLUMN] = {"invalid_count": len(invalid), "invalid_values": invalid.unique().tolist()}
    return issues


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """Apply deterministic type/name checks without dropping or reordering records."""
    cleaned = normalize_column_names(df)
    if ROW_ID_COLUMN not in cleaned.columns or not cleaned[ROW_ID_COLUMN].is_unique:
        raise ValueError(f"{ROW_ID_COLUMN} must exist and be unique before cleaning.")
    if TARGET_COLUMN not in cleaned.columns:
        raise KeyError(f"Target column {TARGET_COLUMN!r} not found.")
    converted = pd.to_numeric(cleaned[TARGET_COLUMN], errors="raise")
    if not set(converted.unique()).issubset({0, 1}):
        raise ValueError(f"Target column {TARGET_COLUMN!r} must be binary 0/1.")
    cleaned[TARGET_COLUMN] = converted.astype("int64")
    return cleaned


def _content_groups(df: pd.DataFrame) -> pd.Series:
    content = df.drop(columns=[ROW_ID_COLUMN], errors="ignore")
    return pd.util.hash_pandas_object(content, index=False).astype(str)


def assert_split_integrity(source_df: pd.DataFrame, train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
    source_ids = set(source_df[ROW_ID_COLUMN])
    train_ids = set(train_df[ROW_ID_COLUMN])
    val_ids = set(val_df[ROW_ID_COLUMN])
    test_ids = set(test_df[ROW_ID_COLUMN])
    assert len(source_ids) == len(source_df), "Source row_id values are not unique."
    assert train_ids.isdisjoint(val_ids), "Train and validation row_id overlap."
    assert train_ids.isdisjoint(test_ids), "Train and test row_id overlap."
    assert val_ids.isdisjoint(test_ids), "Validation and test row_id overlap."
    assert train_ids | val_ids | test_ids == source_ids, "Split does not cover every source row_id exactly once."
    assert len(train_ids) + len(val_ids) + len(test_ids) == len(source_ids), "Split contains repeated row_id values."


def build_train_validation_split(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN,
    test_size: float = 0.2,
    val_size: float = 0.25,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Create reproducible ~60/20/20 stratified, duplicate-content-grouped splits."""
    if target_col not in df.columns:
        raise KeyError(f"Không tìm thấy cột nhãn {target_col!r}.")
    if ROW_ID_COLUMN not in df.columns or not df[ROW_ID_COLUMN].is_unique:
        raise ValueError(f"{ROW_ID_COLUMN} must exist and be unique before splitting.")
    if not np.isclose(test_size, 0.2) or not np.isclose(val_size, 0.25):
        raise ValueError("Grouped Week 2 split currently supports the documented 60/20/20 ratio only.")
    from sklearn.model_selection import StratifiedGroupKFold

    groups = _content_groups(df)
    splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=random_state)
    fold = np.full(len(df), -1, dtype=int)
    for fold_number, (_, held_out) in enumerate(splitter.split(df, df[target_col], groups)):
        fold[held_out] = fold_number
    if (fold < 0).any():
        raise AssertionError("At least one record was not assigned to a split fold.")
    test_df = df.iloc[np.flatnonzero(fold == 0)].copy().reset_index(drop=True)
    val_df = df.iloc[np.flatnonzero(fold == 1)].copy().reset_index(drop=True)
    train_df = df.iloc[np.flatnonzero(fold >= 2)].copy().reset_index(drop=True)
    assert_split_integrity(df, train_df, val_df, test_df)
    return train_df, val_df, test_df


def split_features_target(df: pd.DataFrame, target_col: str = TARGET_COLUMN, feature_columns: list[str] | None = None) -> tuple[pd.DataFrame, pd.Series]:
    """Return the approved Week 3 matrix and target; never infer eligibility."""
    if target_col not in df.columns:
        raise KeyError(f"Target column {target_col!r} not found.")
    if feature_columns is None:
        from src.features import CONFIRMED_MODEL_FEATURES
        feature_columns = CONFIRMED_MODEL_FEATURES
    forbidden = {target_col, ROW_ID_COLUMN}
    if forbidden & set(feature_columns):
        raise ValueError(f"Feature list contains forbidden columns: {sorted(forbidden & set(feature_columns))}")
    missing = [column for column in feature_columns if column not in df.columns]
    if missing:
        raise KeyError(f"Requested feature columns not found: {missing}")
    return df[feature_columns].copy(), df[target_col].copy()


def summarize_dataset(df: pd.DataFrame) -> dict[str, Any]:
    return {
        "shape": df.shape,
        "missing_values": df.isna().sum().to_dict(),
        "target_distribution": df[TARGET_COLUMN].value_counts(normalize=True).sort_index().to_dict(),
        "duplicates": check_duplicates(df),
    }
