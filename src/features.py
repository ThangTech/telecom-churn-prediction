"""Feature eligibility decided from Week 2 evidence."""

TARGET = "Churn"
TECHNICAL_COLUMNS = ["row_id"]
PENDING_VERIFICATION_FEATURES = []

# Week 4 audit metadata. The list below preserves the exact 13 inputs used by
# the frozen evaluation; the correction did not alter the fitted model or rerun test.
WEEK4_AUDIT_FEATURE_SET_STATUS = "FINAL"
WEEK4_TEMPORAL_DECISIONS = {
    "Status": "KEEP",
    "Customer Value": "KEEP",
}

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


def feature_eligibility() -> dict[str, object]:
    return {
        "confirmed_model_features": CONFIRMED_MODEL_FEATURES.copy(),
        "target": TARGET,
        "technical_columns": TECHNICAL_COLUMNS.copy(),
        "pending_verification": PENDING_VERIFICATION_FEATURES.copy(),
        "week4_audit_feature_set_status": WEEK4_AUDIT_FEATURE_SET_STATUS,
        "week4_temporal_decisions": WEEK4_TEMPORAL_DECISIONS.copy(),
    }
