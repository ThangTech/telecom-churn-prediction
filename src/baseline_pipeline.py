"""Thang's baseline pipeline; metadata-dependent results remain provisional."""
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.features import CONFIRMED_MODEL_FEATURES

CATEGORICAL = ["Complains", "Age Group", "Tariff Plan", "Status"]
NUMERIC = [name for name in CONFIRMED_MODEL_FEATURES if name not in CATEGORICAL]


def make_pipeline(class_weight=None, C=1.0, seed=42):
    numeric = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
    categorical = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])
    preprocessor = ColumnTransformer([("numeric", numeric, NUMERIC), ("categorical", categorical, CATEGORICAL)])
    return Pipeline([
        ("preprocessing", preprocessor),
        ("model", LogisticRegression(C=C, class_weight=class_weight, max_iter=3000, random_state=seed)),
    ])
