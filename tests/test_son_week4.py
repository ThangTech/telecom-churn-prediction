from __future__ import annotations

import json
import hashlib
import unittest
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.data import basic_cleaning, build_train_validation_split, load_raw_data
from src.features import (
    CONFIRMED_MODEL_FEATURES,
    WEEK4_AUDIT_FEATURE_SET_STATUS,
    WEEK4_TEMPORAL_DECISIONS,
)
from src.week4_analysis import extract_logistic_coefficients, fit_tertile_edges

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/week4_frozen_evaluation.json"


class Week4FrozenArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_frozen_config_has_required_keys(self):
        required = {
            "raw_sha256",
            "seed",
            "split_manifest",
            "features",
            "preprocessing",
            "model",
            "primary_metric",
            "capacity_thresholds",
            "primary_threshold",
            "test_evaluated",
            "test_evaluation_count",
            "feature_set_status",
            "cv_result_source",
            "temporal_audit",
            "threshold_source",
            "threshold_refit_protocol",
        }
        self.assertTrue(required.issubset(self.config))
        self.assertEqual(self.config["features"], CONFIRMED_MODEL_FEATURES)
        manifest = ROOT / self.config["split_manifest"]
        self.assertTrue(manifest.exists())
        self.assertEqual(hashlib.sha256(manifest.read_bytes()).hexdigest(), self.config["split_manifest_sha256"])

    def test_candidate_and_cv_artifacts_match_the_13_feature_rerun(self):
        experiment = json.loads((ROOT / "configs/experiments.json").read_text(encoding="utf-8"))
        folds = pd.read_csv(ROOT / "reports/week3_cv_folds.csv")
        self.assertEqual(experiment["features"], CONFIRMED_MODEL_FEATURES)
        self.assertEqual(len(experiment["features"]), 13)
        self.assertEqual(experiment["selected"]["run"], "B1_C10")
        self.assertEqual(experiment["selected"]["C"], 10.0)
        self.assertEqual(experiment["selected"]["class_weight"], "none")
        self.assertEqual(len(folds), 30)
        self.assertTrue((folds.groupby("run")["fold"].nunique() == 5).all())

    def test_temporal_decisions_are_consistent_with_final_status(self):
        self.assertEqual(WEEK4_AUDIT_FEATURE_SET_STATUS, "FINAL")
        self.assertEqual(self.config["feature_set_status"], "FINAL")
        self.assertEqual(WEEK4_TEMPORAL_DECISIONS["Status"], "KEEP")
        self.assertEqual(WEEK4_TEMPORAL_DECISIONS["Customer Value"], "KEEP")
        self.assertEqual(self.config["temporal_audit"]["Status"]["decision"], "KEEP")
        self.assertEqual(self.config["temporal_audit"]["Customer Value"]["decision"], "KEEP")
        self.assertTrue(self.config["temporal_audit"]["Customer Value"]["included_in_evaluated_artifact"])

    def test_threshold_source_and_final_fit_are_explicit(self):
        self.assertIn("validation", self.config["threshold_source"])
        self.assertNotIn("test", self.config["threshold_source"])
        self.assertEqual(self.config["final_fit_partition"], "train+validation")
        self.assertIn("train+validation", self.config["threshold_refit_protocol"])
        self.assertTrue(self.config["threshold_validity_after_final_fit"].startswith("VALID AS FROZEN"))

    def test_model_card_matches_corrected_frozen_config(self):
        card = (ROOT / "docs/model-card-draft.md").read_text(encoding="utf-8")
        self.assertIn("PASS / FINAL", card)
        self.assertIn("Customer Value is KEEP", card)
        self.assertIn("capacity interpretation is approximate", card)
        self.assertEqual(self.config["test_evaluation_count"], 1)

    def test_constant_baseline_interpretation_note_exists(self):
        report = (ROOT / "reports/week4-son-analysis.md").read_text(encoding="utf-8")
        self.assertIn("degenerate constant-score", report)
        self.assertIn("AP=0.157143", report)
        self.assertIn("ROC_AUC=0.5", report)
        self.assertIn("endpoint geometry", self.config["baseline_pr_auc_note"])

    def test_final_evaluation_transition_is_recorded_once(self):
        self.assertEqual(self.config["status"], "final_test_evaluated")
        self.assertIs(self.config["test_evaluated"], True)
        self.assertEqual(self.config["test_evaluation_count"], 1)
        self.assertIn("test_evaluation_started_utc", self.config)
        self.assertIn("test_evaluated_utc", self.config)
        self.assertIs(self.config["test_decisions_changed_after_evaluation"], False)

    def test_capacity_thresholds_are_bounded_and_ordered(self):
        rows = self.config["capacity_thresholds"]
        self.assertEqual([row["capacity_level"] for row in rows], ["LOW", "MEDIUM", "HIGH"])
        values = [row["threshold"] for row in rows]
        self.assertTrue(all(0.0 <= value <= 1.0 for value in values))
        self.assertEqual(values, sorted(values, reverse=True))

    def test_final_metrics_are_finite_and_bounded(self):
        final = pd.read_csv(ROOT / "reports/week4_test_final.csv").iloc[0]
        for metric in ["AP", "PR_AUC", "ROC_AUC", "Brier", "precision", "recall", "F1"]:
            self.assertTrue(np.isfinite(final[metric]))
            self.assertGreaterEqual(final[metric], 0.0)
            self.assertLessEqual(final[metric], 1.0)
        self.assertEqual(final["evaluation_partition"], "test")
        self.assertEqual(int(final["n_samples"]), 630)

    def test_coefficient_extraction_matches_transformed_width(self):
        model = joblib.load(ROOT / "models/week4_final_candidate.joblib")
        coefficients = extract_logistic_coefficients(model)
        preprocessing = model.named_steps["preprocessing"]
        self.assertEqual(len(coefficients), len(preprocessing.get_feature_names_out()))
        self.assertEqual(len(coefficients), len(pd.read_csv(ROOT / "reports/week4_coefficients.csv")))

    def test_error_group_boundaries_use_predictors_only(self):
        values = pd.Series([1, 2, 3, 4, 5, 6])
        first = fit_tertile_edges(values)
        shuffled_target = pd.Series([1, 0, 1, 0, 0, 1]).sample(frac=1, random_state=9)
        second = fit_tertile_edges(values)
        self.assertEqual(first, second)
        self.assertEqual(len(shuffled_target), len(values))

    def test_final_pipeline_does_not_refit_on_validation_prediction(self):
        model = joblib.load(ROOT / "models/week4_final_candidate.joblib")
        preprocessing = model.named_steps["preprocessing"]
        scaler = preprocessing.named_transformers_["numeric"].named_steps["scaler"]
        encoder = preprocessing.named_transformers_["categorical"].named_steps["encoder"]
        mean_before = scaler.mean_.copy()
        categories_before = [item.copy() for item in encoder.categories_]

        raw = basic_cleaning(load_raw_data(ROOT / "data/raw/Customer Churn.csv"))
        _, validation, _ = build_train_validation_split(raw, random_state=42)
        probability = model.predict_proba(validation[CONFIRMED_MODEL_FEATURES])[:, 1]

        self.assertTrue(np.isfinite(probability).all())
        self.assertTrue(((probability >= 0.0) & (probability <= 1.0)).all())
        np.testing.assert_array_equal(mean_before, scaler.mean_)
        for before, after in zip(categories_before, encoder.categories_):
            np.testing.assert_array_equal(before, after)

    def test_error_reports_cover_each_test_record_once(self):
        for name in ["week4_error_by_tenure.csv", "week4_error_by_charge.csv"]:
            report = pd.read_csv(ROOT / "reports" / name)
            self.assertEqual(report["n_samples"].sum(), 630)
            self.assertEqual(set(report["group"]), {"low", "medium", "high"})


if __name__ == "__main__":
    unittest.main()
