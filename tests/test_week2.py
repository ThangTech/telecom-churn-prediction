from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.data import (
    ROW_ID_COLUMN,
    assert_split_integrity,
    basic_cleaning,
    build_train_validation_split,
    load_data_dictionary,
    load_raw_data,
    split_features_target,
    validate_schema,
)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Customer Churn.csv"
DICTIONARY = ROOT / "data" / "data_dictionary.csv"


class DictionaryTests(unittest.TestCase):
    def _write_dictionary(self, frame: pd.DataFrame) -> Path:
        temp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
        temp.close()
        path = Path(temp.name)
        frame.to_csv(path, index=False)
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def test_wrong_dictionary_key_raises(self):
        frame = pd.DataFrame({"field_name": ["Churn"], "data_type": ["integer"], "description": ["target"], "role": ["target"]})
        with self.assertRaisesRegex(ValueError, "column_name"):
            load_data_dictionary(self._write_dictionary(frame))

    def test_exactly_one_churn_target_required(self):
        valid = load_data_dictionary(DICTIONARY)
        no_target = valid.assign(role="feature")
        with self.assertRaisesRegex(ValueError, "exactly one target"):
            load_data_dictionary(self._write_dictionary(no_target))
        two_targets = pd.concat([valid, valid.loc[valid["column_name"] == "Churn"].assign(column_name="OtherTarget")])
        with self.assertRaisesRegex(ValueError, "exactly one target"):
            load_data_dictionary(self._write_dictionary(two_targets))

    def test_duplicate_dictionary_column_and_invalid_role_raise(self):
        valid = load_data_dictionary(DICTIONARY)
        duplicate = pd.concat([valid, valid.iloc[[0]]], ignore_index=True)
        with self.assertRaisesRegex(ValueError, "Duplicate column_name"):
            load_data_dictionary(self._write_dictionary(duplicate))
        invalid_role = valid.copy()
        invalid_role.loc[0, "role"] = "identifier"
        with self.assertRaisesRegex(ValueError, "Invalid data dictionary roles"):
            load_data_dictionary(self._write_dictionary(invalid_role))

    def test_schema_mismatch_raises(self):
        data = load_raw_data(RAW).drop(columns=["Age"])
        dictionary = load_data_dictionary(DICTIONARY)
        with self.assertRaisesRegex(ValueError, "Schema validation failed"):
            validate_schema(data, dictionary=dictionary)


class IdentityAndSplitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = load_raw_data(RAW)
        cls.cleaned = basic_cleaning(cls.raw)

    def test_row_id_is_stable_unique_and_preserved(self):
        again = load_raw_data(RAW)
        self.assertTrue(self.raw[ROW_ID_COLUMN].is_unique)
        self.assertListEqual(self.raw[ROW_ID_COLUMN].tolist(), again[ROW_ID_COLUMN].tolist())
        self.assertEqual(len(self.cleaned), len(self.raw))

    def test_split_is_disjoint_complete_and_reproducible(self):
        first = build_train_validation_split(self.cleaned, random_state=42)
        second = build_train_validation_split(self.cleaned, random_state=42)
        assert_split_integrity(self.cleaned, *first)
        for left, right in zip(first, second):
            self.assertListEqual(left[ROW_ID_COLUMN].tolist(), right[ROW_ID_COLUMN].tolist())
            self.assertEqual(set(left["Churn"]), {0, 1})

    def test_duplicate_content_does_not_cross_splits(self):
        splits = build_train_validation_split(self.cleaned, random_state=42)
        keys = [set(pd.util.hash_pandas_object(part.drop(columns=[ROW_ID_COLUMN]), index=False)) for part in splits]
        self.assertTrue(keys[0].isdisjoint(keys[1]))
        self.assertTrue(keys[0].isdisjoint(keys[2]))
        self.assertTrue(keys[1].isdisjoint(keys[2]))

    def test_target_and_row_id_are_not_features(self):
        train, _, _ = build_train_validation_split(self.cleaned, random_state=42)
        features, target = split_features_target(train)
        self.assertNotIn("Churn", features.columns)
        self.assertNotIn(ROW_ID_COLUMN, features.columns)
        self.assertNotIn("Status", features.columns)
        self.assertNotIn("Customer Value", features.columns)
        self.assertEqual(target.name, "Churn")


if __name__ == "__main__":
    unittest.main()
