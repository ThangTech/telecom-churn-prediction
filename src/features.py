"""Feature eligibility decided from Week 2 evidence."""

TARGET = "Churn"
TECHNICAL_COLUMNS = ["row_id"]
PENDING_VERIFICATION_FEATURES = []

CONFIRMED_MODEL_FEATURES = [
    "Call  Failure",
    "Complains",
    "Subscription  Length",
    "Charge  Amount",
    "Seconds of Use",
    "Frequency of use",
    "Frequency of SMS",
    "Distinct Called Numbers",
    "Age Group",
    "Tariff Plan",
    "Status",
    "Age",
    "Customer Value",
]


def feature_eligibility() -> dict[str, list[str] | str]:
    return {
        "confirmed_model_features": CONFIRMED_MODEL_FEATURES.copy(),
        "target": TARGET,
        "technical_columns": TECHNICAL_COLUMNS.copy(),
        "pending_verification": PENDING_VERIFICATION_FEATURES.copy(),
    }
