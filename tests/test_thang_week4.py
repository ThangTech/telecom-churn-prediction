import unittest

from scripts.verify_week4_thang import verify_week4
from src.baseline_pipeline import CATEGORICAL


class ThangWeek4AcceptanceTests(unittest.TestCase):
    def test_status_is_reproduced_as_a_categorical_feature(self):
        self.assertIn("Status", CATEGORICAL)

    def test_frozen_week4_artifacts_pass_acceptance_audit(self):
        result = verify_week4()
        self.assertEqual(result["status"], "PASS", result["failed_checks"])
        self.assertTrue(all(result["checks"].values()))


if __name__ == "__main__":
    unittest.main()
