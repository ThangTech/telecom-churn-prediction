from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from src.features import (
    CONFIRMED_MODEL_FEATURES,
    PENDING_VERIFICATION_FEATURES,
    TARGET,
    TECHNICAL_COLUMNS,
)

try:
    from scripts.baseline_common import ROOT, model_inputs, prepare_data
    from src.baseline_pipeline import make_pipeline
except ModuleNotFoundError:
    ROOT = Path(__file__).resolve().parents[1]
    THANG_WEEK3_AVAILABLE = False
else:
    THANG_WEEK3_AVAILABLE = True


class SonFeatureEligibilityTests(unittest.TestCase):
    def test_provisional_feature_set_excludes_target_technical_and_pending(self):
        confirmed = set(CONFIRMED_MODEL_FEATURES)
        self.assertNotIn(TARGET, confirmed)
        self.assertTrue(confirmed.isdisjoint(TECHNICAL_COLUMNS))
        self.assertTrue(confirmed.isdisjoint(PENDING_VERIFICATION_FEATURES))
        self.assertEqual(len(CONFIRMED_MODEL_FEATURES), 11)


@unittest.skipUnless(
    THANG_WEEK3_AVAILABLE,
    "Week 3 implementation is on origin/Thang and has not been integrated into branch Son.",
)
class SonWeek3ReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (cls.train, cls.validation, cls.test), _ = prepare_data()
        cls.X_train, cls.y_train = model_inputs(cls.train)
        cls.X_validation, cls.y_validation = model_inputs(cls.validation)
        cls.pipeline = make_pipeline(class_weight=None, C=10.0)
        cls.pipeline.fit(cls.X_train, cls.y_train)

    def test_encoder_and_scaler_are_not_refit_during_validation_prediction(self):
        preprocessing = self.pipeline.named_steps["preprocessing"]
        numeric = preprocessing.named_transformers_["numeric"]
        categorical = preprocessing.named_transformers_["categorical"]
        scaler_before = numeric.named_steps["scaler"].mean_.copy()
        categories_before = [values.copy() for values in categorical.named_steps["encoder"].categories_]

        validation = self.X_validation.copy()
        validation.loc[validation.index[0], "Tariff Plan"] = 999
        self.pipeline.predict_proba(validation)

        np.testing.assert_array_equal(scaler_before, numeric.named_steps["scaler"].mean_)
        for before, after in zip(categories_before, categorical.named_steps["encoder"].categories_):
            np.testing.assert_array_equal(before, after)

    def test_validation_probabilities_are_finite_and_bounded(self):
        probabilities = self.pipeline.predict_proba(self.X_validation)[:, 1]
        self.assertTrue(np.isfinite(probabilities).all())
        self.assertTrue(((probabilities >= 0.0) & (probabilities <= 1.0)).all())

    def test_train_cv_folds_have_no_row_or_duplicate_content_overlap(self):
        groups = pd.util.hash_pandas_object(
            self.train.drop(columns="row_id"), index=False
        ).astype(str)
        folds = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
        for fit_idx, heldout_idx in folds.split(self.X_train, self.y_train, groups):
            self.assertTrue(
                set(self.train.iloc[fit_idx]["row_id"]).isdisjoint(
                    set(self.train.iloc[heldout_idx]["row_id"])
                )
            )
            self.assertTrue(set(groups.iloc[fit_idx]).isdisjoint(set(groups.iloc[heldout_idx])))

    def test_artifacts_explicitly_record_test_as_untouched(self):
        config = json.loads((ROOT / "configs" / "experiments.json").read_text(encoding="utf-8"))
        self.assertIs(config["test_evaluated"], False)
        validation = pd.read_csv(ROOT / "reports" / "week3_validation.csv")
        self.assertTrue((validation["n_samples"] == len(self.validation)).all())


if __name__ == "__main__":
    unittest.main()
