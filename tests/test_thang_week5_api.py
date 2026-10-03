import math
import unittest

try:
    from fastapi.testclient import TestClient
except ImportError:  # Lets the ML-only test suite explain the optional dependency.
    TestClient = None

from src.features import CONFIRMED_MODEL_FEATURES


VALID_FEATURES = {
    "Call  Failure": 1,
    "Complains": 0,
    "Subscription  Length": 24,
    "Charge  Amount": 2,
    "Seconds of Use": 1000,
    "Frequency of use": 80,
    "Frequency of SMS": 12,
    "Distinct Called Numbers": 20,
    "Age Group": 3,
    "Tariff Plan": 1,
    "Status": 1,
    "Age": 35,
    "Customer Value": 42.75,
}


@unittest.skipIf(TestClient is None, "Install app/backend/requirements.txt to run API tests")
class ThangWeek5ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from app.backend.main import app

        cls.client = TestClient(app)

    def test_health_reports_loaded_frozen_model(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["feature_count"], 13)
        self.assertTrue(payload["model_version"].startswith("week4-final-"))

    def test_valid_request_matches_frontend_contract_for_each_mode(self):
        expected_thresholds = {
            "LOW": 0.47683299575833915,
            "MEDIUM": 0.3431830803885034,
            "HIGH": 0.16505680661293284,
        }
        for mode, expected_threshold in expected_thresholds.items():
            with self.subTest(mode=mode):
                response = self.client.post(
                    "/api/churn-score",
                    json={"features": VALID_FEATURES, "capacity_mode": mode},
                )
                self.assertEqual(response.status_code, 200, response.text)
                payload = response.json()
                self.assertEqual(payload["capacity_mode"], mode)
                self.assertAlmostEqual(payload["threshold"], expected_threshold)
                self.assertTrue(math.isfinite(payload["churn_probability"]))
                self.assertGreaterEqual(payload["churn_probability"], 0.0)
                self.assertLessEqual(payload["churn_probability"], 1.0)
                self.assertEqual(
                    payload["predicted_churn"],
                    payload["churn_probability"] >= payload["threshold"],
                )
                self.assertIn(payload["priority_group"], {"HIGH", "MEDIUM", "EXTENDED", "NOT_PRIORITIZED"})
                self.assertTrue(payload["request_id"])

    def test_feature_schema_is_exactly_the_frozen_13_columns(self):
        self.assertEqual(list(VALID_FEATURES), CONFIRMED_MODEL_FEATURES)

        missing = dict(VALID_FEATURES)
        missing.pop("Age")
        response = self.client.post("/api/churn-score", json={"features": missing, "capacity_mode": "MEDIUM"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["code"], "INVALID_FEATURE_VALUE")

        extra = {**VALID_FEATURES, "Churn": 1}
        response = self.client.post("/api/churn-score", json={"features": extra, "capacity_mode": "MEDIUM"})
        self.assertEqual(response.status_code, 422)

    def test_invalid_types_ranges_and_mode_are_rejected(self):
        invalid_cases = [
            ("Age Group", 6),
            ("Tariff Plan", 3),
            ("Status", 0),
            ("Charge  Amount", 10),
            ("Age", -1),
            ("Frequency of SMS", 1.5),
            ("Complains", True),
            ("Customer Value", "NaN"),
        ]
        for feature, value in invalid_cases:
            with self.subTest(feature=feature, value=value):
                request = dict(VALID_FEATURES)
                request[feature] = value
                response = self.client.post(
                    "/api/churn-score",
                    json={"features": request, "capacity_mode": "MEDIUM"},
                )
                self.assertEqual(response.status_code, 422, response.text)
                self.assertEqual(response.json()["code"], "INVALID_FEATURE_VALUE")

        response = self.client.post(
            "/api/churn-score",
            json={"features": VALID_FEATURES, "capacity_mode": "UNKNOWN"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["code"], "INVALID_REQUEST")

    def test_cors_allows_only_configured_local_frontend(self):
        allowed = self.client.options(
            "/api/churn-score",
            headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"},
        )
        self.assertEqual(allowed.status_code, 200)
        self.assertEqual(allowed.headers.get("access-control-allow-origin"), "http://localhost:5173")

        blocked = self.client.options(
            "/api/churn-score",
            headers={"Origin": "https://example.invalid", "Access-Control-Request-Method": "POST"},
        )
        self.assertNotEqual(blocked.headers.get("access-control-allow-origin"), "https://example.invalid")


if __name__ == "__main__":
    unittest.main()
