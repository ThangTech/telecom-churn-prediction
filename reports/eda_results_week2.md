# Week 2 EDA Results — Train Only

Canonical command: `python scripts/eda_train.py`.

## Scope guard

- Analytical input: train split only (1,890 rows).
- Validation and test are not inspected for distributions, correlations, feature selection, preprocessing, thresholds, or class weights.
- No preprocessing transformer is fitted by this script.

## Data checks

- Missing values in train: 0
- Excess duplicate-content rows within train: 179
- Duplicate contents were retained. The grouped splitter prevents identical content crossing split boundaries.

## Target distribution

| Churn | count |
|---:|---:|
| 0 | 1593 |
| 1 | 297 |

**Purpose:** quantify class balance on train before modeling.

**Finding:** Train churn rate is 15.71%; the classes are imbalanced.

**Limitation:** this is one split and contains no performance evidence.

**Allowed conclusion:** use stratification and compare `class_weight=None` with `class_weight="balanced"` using validation only.

## Descriptive statistics

```text
       Subscription  Length  Charge  Amount  Complains
count              1890.000        1890.000   1890.000
mean                 32.465           0.932      0.072
std                   8.774           1.531      0.259
min                   3.000           0.000      0.000
25%                  29.000           0.000      0.000
50%                  35.000           0.000      0.000
75%                  38.000           1.000      0.000
max                  47.000          10.000      1.000
```

## Required feature distributions

Artifact: `reports/figures/key_feature_distributions.png`

**Purpose:** inspect scale, skew and class-conditional distributions for Subscription Length, Charge Amount and Complains.

**Finding:** The three required variables have different ranges and non-Gaussian shapes; scaling should be fitted inside the training pipeline.

**Limitation:** visual differences are associations, not causal effects. IQR/extreme values are not automatically errors.

**Allowed conclusion:** use a train-fitted scaler inside the Logistic Regression pipeline; do not delete rows solely from these plots.

## Correlation heatmap

Artifact: `reports/figures/correlation_matrix.png`

**Purpose:** summarize pairwise linear association on train.

**Finding:** The heatmap identifies linear associations worth checking for redundancy; it does not establish causation or leakage.

**Limitation:** correlation misses nonlinear relationships and cannot determine feature availability at prediction time.

**Allowed conclusion:** use it as descriptive evidence only, never as a leakage rule.

## Pending-verification features

Artifact: `reports/figures/pending_features_descriptive.png`

**Purpose:** document train-only distributions without making an eligibility decision.

**Finding:** Both variables show statistical patterns, but their definitions and availability before prediction remain unverified.

**Limitation:** repository metadata does not define how or when either variable is produced.

**Allowed conclusion:** `Status` and `Customer Value` remain excluded from the default model feature set until authoritative temporal evidence is recorded.

## Artifacts

- `reports/figures/target_distribution.png`
- `reports/figures/key_feature_distributions.png`
- `reports/figures/correlation_matrix.png`
- `reports/figures/pending_features_descriptive.png`
