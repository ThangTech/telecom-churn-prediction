import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.features import PENDING_VERIFICATION_FEATURES
import joblib
import numpy as np
import pandas as pd

from scripts.baseline_common import model_inputs, prepare_data
from src.baseline_pipeline import NUMERIC, make_pipeline
from src.metrics import evaluate_probabilities


class BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (cls.train, cls.validation, _), cls.manifest = prepare_data()

    def test_constant_score_has_no_ranking_ability(self):
        y = np.array([0, 0, 0, 1])
        metrics = evaluate_probabilities(y, np.full(4, 0.2))
        self.assertAlmostEqual(metrics['ROC_AUC'], 0.5)
        self.assertAlmostEqual(metrics['AP'], 0.25)
        self.assertFalse(metrics['precision_defined'])
        self.assertEqual(metrics['FN'], 1)

    def test_preprocessing_learns_only_training_statistics(self):
        X, y = model_inputs(self.train)
        X = X.copy()
        X.loc[X.index[0], NUMERIC[0]] = np.nan
        pipeline = make_pipeline()
        pipeline.fit(X, y)
        numeric = pipeline.named_steps['preprocessing'].named_transformers_['numeric']
        expected = X[NUMERIC].median().to_numpy()
        np.testing.assert_allclose(numeric.named_steps['imputer'].statistics_, expected)
        heldout, _ = model_inputs(self.validation)
        heldout[NUMERIC] = 10000000
        heldout['Tariff Plan'] = 999  # New category is handled without refitting.
        before = numeric.named_steps['scaler'].mean_.copy()
        probabilities = pipeline.predict_proba(heldout)[:, 1]
        np.testing.assert_array_equal(before, numeric.named_steps['scaler'].mean_)
        self.assertTrue(np.isfinite(probabilities).all())

    def test_feature_inputs_exclude_target_identity_and_pending_variables(self):
        X, _ = model_inputs(self.train)

        forbidden = {'Churn', 'row_id'} | set(PENDING_VERIFICATION_FEATURES)

        self.assertFalse(set(X.columns) & forbidden)

    def test_invalid_probability_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_probabilities([0, 1], [0.2, 1.2])

    def test_pipeline_round_trip_preserves_probabilities(self):
        X, y = model_inputs(self.train)
        pipeline = make_pipeline()
        pipeline.fit(X, y)
        heldout, _ = model_inputs(self.validation)
        heldout = heldout.head(8).copy()
        heldout['Tariff Plan'] = 999  # Exercise handle_unknown="ignore" after reload.
        expected = pipeline.predict_proba(heldout)

        with TemporaryDirectory() as directory:
            model_path = Path(directory) / 'pipeline.joblib'
            joblib.dump(pipeline, model_path)
            restored = joblib.load(model_path)
            actual = restored.predict_proba(heldout)

        np.testing.assert_allclose(actual, expected)


if __name__ == '__main__':
    unittest.main()
