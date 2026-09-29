"""
Week 2 EDA — Iranian Churn Dataset
TRAIN SET ONLY — No test/validation contamination
Author: Son (Team Member 2)
"""
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from src.data import (
    load_raw_data,
    basic_cleaning,
    build_train_validation_split,
    TARGET_COLUMN,
)

FIGURES_DIR = Path("reports/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 1. LOAD & VERIFY DATASET
# ==============================================================================
print("=" * 80)
print("SECTION 1: DATASET VERIFICATION")
print("=" * 80)

raw_df = load_raw_data("data/raw/Customer Churn.csv")
print(f"Raw shape: {raw_df.shape}")
print(f"Columns: {raw_df.columns.tolist()}")
print(f"Dtypes:\n{raw_df.dtypes}")
print(f"\nMissing values:\n{raw_df.isna().sum()}")
print(f"\nTotal missing: {raw_df.isna().sum().sum()}")
print(f"Exact duplicate rows (raw): {raw_df.duplicated().sum()}")
print(f"\nChurn distribution (raw):")
print(raw_df["Churn"].value_counts().sort_index())
print(f"Churn rate (raw): {raw_df['Churn'].mean():.4f} ({raw_df['Churn'].mean()*100:.2f}%)")

# ==============================================================================
# 2. CLEAN & SPLIT
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 2: CLEANING & SPLIT")
print("=" * 80)

cleaned_df = basic_cleaning(raw_df)
print(f"After cleaning: {cleaned_df.shape}")
print(f"Rows removed (duplicates): {len(raw_df) - len(cleaned_df)}")
print(f"Churn rate (cleaned): {cleaned_df['Churn'].mean():.4f} ({cleaned_df['Churn'].mean()*100:.2f}%)")

train_df, val_df, test_df = build_train_validation_split(cleaned_df)

total = len(cleaned_df)
print(f"\n--- SPLIT RESULTS ---")
print(f"Train: {len(train_df)} rows ({len(train_df)/total*100:.1f}%)")
print(f"Val:   {len(val_df)} rows ({len(val_df)/total*100:.1f}%)")
print(f"Test:  {len(test_df)} rows ({len(test_df)/total*100:.1f}%)")
print(f"Total: {len(train_df)+len(val_df)+len(test_df)} (should be {total})")

print(f"\n--- STRATIFICATION CHECK ---")
print(f"Full  churn rate: {cleaned_df['Churn'].mean():.4f}")
print(f"Train churn rate: {train_df['Churn'].mean():.4f}")
print(f"Val   churn rate: {val_df['Churn'].mean():.4f}")
print(f"Test  churn rate: {test_df['Churn'].mean():.4f}")

# Overlap check
train_idx = set(train_df.index)
val_idx = set(val_df.index)
test_idx = set(test_df.index)
overlap_tv = train_idx & val_idx
overlap_tt = train_idx & test_idx
overlap_vt = val_idx & test_idx
print(f"\n--- OVERLAP CHECK ---")
print(f"Train-Val overlap:  {len(overlap_tv)} (should be 0)")
print(f"Train-Test overlap: {len(overlap_tt)} (should be 0)")
print(f"Val-Test overlap:   {len(overlap_vt)} (should be 0)")
overlap_pass = len(overlap_tv) == 0 and len(overlap_tt) == 0 and len(overlap_vt) == 0
print(f"OVERLAP CHECK: {'PASS' if overlap_pass else 'FAIL'}")

# ==============================================================================
# 3. TRAIN SET OVERVIEW
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 3: TRAIN SET OVERVIEW")
print("=" * 80)

print(f"Shape: {train_df.shape}")
print(f"\nColumns and dtypes:")
for col in train_df.columns:
    print(f"  {col}: {train_df[col].dtype} | unique={train_df[col].nunique()} | nulls={train_df[col].isna().sum()}")

print(f"\nMemory: {train_df.memory_usage(deep=True).sum() / 1024:.1f} KB")

# ==============================================================================
# 4. TARGET DISTRIBUTION
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 4: TARGET DISTRIBUTION (TRAIN)")
print("=" * 80)

target_counts = train_df[TARGET_COLUMN].value_counts().sort_index()
target_pct = train_df[TARGET_COLUMN].value_counts(normalize=True).sort_index()
for val in sorted(target_counts.index):
    label = "No Churn" if val == 0 else "Churn"
    print(f"  {val} ({label}): {target_counts[val]:,} ({target_pct[val]*100:.2f}%)")

imbalance_ratio = target_counts[0] / target_counts[1]
print(f"\nImbalance ratio (majority/minority): {imbalance_ratio:.1f}:1")
print(f"Class imbalance: {'Moderate' if imbalance_ratio < 10 else 'Severe'}")

# Figure: target distribution
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar([0, 1], [target_counts[0], target_counts[1]],
              color=['#2ecc71', '#e74c3c'], edgecolor='black')
ax.set_xticks([0, 1])
ax.set_xticklabels(['No Churn (0)', 'Churn (1)'])
ax.set_ylabel('Count')
ax.set_title('Target Distribution (Train Set)')
for bar, count, pct in zip(bars, target_counts.values, target_pct.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{count}\n({pct*100:.1f}%)', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "target_distribution.png", dpi=150)
plt.close()
print("Saved: reports/figures/target_distribution.png")

# ==============================================================================
# 5. DESCRIPTIVE STATISTICS
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 5: DESCRIPTIVE STATISTICS (TRAIN)")
print("=" * 80)

print(train_df.describe().round(2).to_string())

# ==============================================================================
# 6. NUMERIC FEATURE DISTRIBUTIONS
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 6: NUMERIC FEATURE DISTRIBUTIONS (TRAIN)")
print("=" * 80)

numeric_cols = [c for c in train_df.select_dtypes(include='number').columns if c != TARGET_COLUMN]
for col in numeric_cols:
    s = train_df[col]
    print(f"\n  {col}:")
    print(f"    min={s.min()}, max={s.max()}, mean={s.mean():.2f}, median={s.median():.2f}, std={s.std():.2f}")
    print(f"    Q1={s.quantile(0.25):.2f}, Q3={s.quantile(0.75):.2f}, IQR={s.quantile(0.75)-s.quantile(0.25):.2f}")
    # Outliers by IQR
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
    n_outliers = ((s < lower) | (s > upper)).sum()
    print(f"    Outliers (IQR): {n_outliers} ({n_outliers/len(s)*100:.1f}%)")

# ==============================================================================
# 7. CATEGORICAL FEATURE DISTRIBUTIONS
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 7: CATEGORICAL-LIKE FEATURES (TRAIN)")
print("=" * 80)

cat_like_cols = [c for c in train_df.columns if c != TARGET_COLUMN and train_df[c].nunique() <= 10]
for col in cat_like_cols:
    print(f"\n  {col} (unique={train_df[col].nunique()}):")
    vc = train_df[col].value_counts().sort_index()
    for v, cnt in vc.items():
        print(f"    {v}: {cnt} ({cnt/len(train_df)*100:.1f}%)")

# ==============================================================================
# 8. CORRELATION MATRIX
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 8: CORRELATION MATRIX (TRAIN)")
print("=" * 80)

corr = train_df.corr(numeric_only=True)
print("\nCorrelation with Churn:")
churn_corr = corr[TARGET_COLUMN].drop(TARGET_COLUMN).sort_values(key=abs, ascending=False)
for feat, val in churn_corr.items():
    print(f"  {feat}: {val:.4f}")

# Figure: correlation matrix
fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, square=True, linewidths=0.5, ax=ax,
            cbar_kws={"shrink": 0.8})
ax.set_title("Correlation Matrix (Train Set)")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "correlation_matrix.png", dpi=150)
plt.close()
print("Saved: reports/figures/correlation_matrix.png")

# ==============================================================================
# 9. FEATURE VS CHURN
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 9: FEATURE VS CHURN (TRAIN)")
print("=" * 80)

for col in numeric_cols:
    grp = train_df.groupby(TARGET_COLUMN)[col].agg(['count', 'mean', 'median', 'std'])
    print(f"\n  {col} by Churn:")
    print(f"    {'Churn':>6} {'Count':>6} {'Mean':>10} {'Median':>10} {'Std':>10}")
    for idx, row in grp.iterrows():
        print(f"    {idx:>6} {int(row['count']):>6} {row['mean']:>10.2f} {row['median']:>10.2f} {row['std']:>10.2f}")

# ==============================================================================
# 10. SCALE DIFFERENCES
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 10: SCALE DIFFERENCES BETWEEN FEATURES (TRAIN)")
print("=" * 80)

scale_info = []
for col in numeric_cols:
    s = train_df[col]
    scale_info.append({
        'Feature': col,
        'Min': s.min(),
        'Max': s.max(),
        'Range': s.max() - s.min(),
        'Mean': s.mean(),
        'Std': s.std()
    })
scale_df = pd.DataFrame(scale_info).sort_values('Range', ascending=False)
print(scale_df.to_string(index=False))
print("\nConclusion: Features have VERY different scales -> Scaling NEEDED for distance-based models")

# ==============================================================================
# 11. STATUS INVESTIGATION
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 11: STATUS INVESTIGATION (TRAIN)")
print("=" * 80)

print("\n--- Cross-tabulation: Status vs Churn ---")
ct = pd.crosstab(train_df["Status"], train_df[TARGET_COLUMN], margins=True)
print(ct)

print("\n--- Churn rate by Status ---")
status_analysis = train_df.groupby("Status")[TARGET_COLUMN].agg(['count', 'sum', 'mean'])
status_analysis.columns = ['customer_count', 'churn_count', 'churn_rate']
print(status_analysis)

print(f"\n--- Point-biserial correlation (Status, Churn) ---")
status_churn_corr = train_df["Status"].corr(train_df[TARGET_COLUMN])
print(f"Correlation: {status_churn_corr:.4f}")

print("\n--- Complains vs Status cross-tab ---")
print(pd.crosstab(train_df["Complains"], train_df["Status"], margins=True))

print("\n--- Status vs other features ---")
for col in ["Complains", "Subscription  Length", "Charge  Amount", "Seconds of Use"]:
    if col in train_df.columns:
        grp = train_df.groupby("Status")[col].mean()
        print(f"  Mean {col} by Status: {dict(grp)}")

# Figure: status_vs_churn
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# Left: count
ct_no_margins = pd.crosstab(train_df["Status"], train_df[TARGET_COLUMN])
ct_no_margins.plot(kind='bar', ax=axes[0], color=['#2ecc71', '#e74c3c'], edgecolor='black')
axes[0].set_title("Status vs Churn (Count)")
axes[0].set_xlabel("Status")
axes[0].set_ylabel("Count")
axes[0].tick_params(axis='x', rotation=0)
axes[0].legend(['No Churn', 'Churn'])
# Right: churn rate
rates = status_analysis['churn_rate']
bars = axes[1].bar(rates.index.astype(str), rates.values, color=['#3498db', '#e67e22'], edgecolor='black')
axes[1].set_title("Churn Rate by Status")
axes[1].set_xlabel("Status")
axes[1].set_ylabel("Churn Rate")
for bar, rate in zip(bars, rates.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                 f'{rate:.1%}', ha='center', fontsize=11)
plt.tight_layout()
plt.savefig(FIGURES_DIR / "status_vs_churn.png", dpi=150)
plt.close()
print("Saved: reports/figures/status_vs_churn.png")

# ==============================================================================
# 12. CUSTOMER VALUE INVESTIGATION
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 12: CUSTOMER VALUE INVESTIGATION (TRAIN)")
print("=" * 80)

cv = train_df["Customer Value"]
print(f"Count: {cv.count()}")
print(f"Unique: {cv.nunique()}")
print(f"Unique ratio: {cv.nunique()/cv.count()*100:.1f}%")
print(f"Min: {cv.min():.3f}")
print(f"Max: {cv.max():.3f}")
print(f"Mean: {cv.mean():.3f}")
print(f"Median: {cv.median():.3f}")
print(f"Std: {cv.std():.3f}")
print(f"\nPercentiles:")
for p in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
    print(f"  P{p}: {cv.quantile(p/100):.3f}")

print(f"\n--- Sequential pattern check ---")
sorted_cv = cv.sort_values().values
diffs = np.diff(sorted_cv)
print(f"Sorted diffs: min={diffs.min():.6f}, max={diffs.max():.3f}, mean={diffs.mean():.3f}, std={diffs.std():.3f}")
is_sequential = np.all(np.abs(diffs - diffs.mean()) < 0.01)
print(f"Sequential (constant step)? {is_sequential}")

print(f"\n--- Customer Value by Churn ---")
cv_by_churn = train_df.groupby(TARGET_COLUMN)["Customer Value"].describe()
print(cv_by_churn.to_string())

print(f"\n--- Correlation with other features ---")
for col in numeric_cols:
    if col != "Customer Value":
        r = train_df["Customer Value"].corr(train_df[col])
        print(f"  Customer Value vs {col}: {r:.4f}")

cv_churn_corr = train_df["Customer Value"].corr(train_df[TARGET_COLUMN])
print(f"\n  Customer Value vs Churn: {cv_churn_corr:.4f}")

# Figure: customer_value_distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(cv, bins=50, color='#3498db', edgecolor='black', alpha=0.7)
axes[0].set_title("Customer Value Distribution (Train)")
axes[0].set_xlabel("Customer Value")
axes[0].set_ylabel("Count")

# Boxplot by churn
train_df.boxplot(column="Customer Value", by=TARGET_COLUMN, ax=axes[1])
axes[1].set_title("Customer Value by Churn")
axes[1].set_xlabel("Churn")
axes[1].set_ylabel("Customer Value")
plt.suptitle("")  # Remove auto-generated suptitle from boxplot
plt.tight_layout()
plt.savefig(FIGURES_DIR / "customer_value_distribution.png", dpi=150)
plt.close()
print("Saved: reports/figures/customer_value_distribution.png")

# Figure: customer_value_vs_churn (detailed)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for churn_val, color, label in [(0, '#2ecc71', 'No Churn'), (1, '#e74c3c', 'Churn')]:
    subset = train_df[train_df[TARGET_COLUMN] == churn_val]["Customer Value"]
    axes[0].hist(subset, bins=50, alpha=0.6, color=color, label=label, edgecolor='black')
axes[0].set_title("Customer Value by Churn Group")
axes[0].set_xlabel("Customer Value")
axes[0].set_ylabel("Count")
axes[0].legend()

# Scatter: Customer Value vs another feature
axes[1].scatter(train_df[train_df[TARGET_COLUMN]==0]["Seconds of Use"],
                train_df[train_df[TARGET_COLUMN]==0]["Customer Value"],
                alpha=0.3, s=10, color='#2ecc71', label='No Churn')
axes[1].scatter(train_df[train_df[TARGET_COLUMN]==1]["Seconds of Use"],
                train_df[train_df[TARGET_COLUMN]==1]["Customer Value"],
                alpha=0.3, s=10, color='#e74c3c', label='Churn')
axes[1].set_xlabel("Seconds of Use")
axes[1].set_ylabel("Customer Value")
axes[1].set_title("Customer Value vs Seconds of Use")
axes[1].legend()
plt.tight_layout()
plt.savefig(FIGURES_DIR / "customer_value_vs_churn.png", dpi=150)
plt.close()
print("Saved: reports/figures/customer_value_vs_churn.png")

# ==============================================================================
# 13. OUTLIER SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 13: OUTLIER SUMMARY (TRAIN)")
print("=" * 80)

for col in numeric_cols:
    s = train_df[col]
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
    n_out = ((s < lower) | (s > upper)).sum()
    if n_out > 0:
        print(f"  {col}: {n_out} outliers ({n_out/len(s)*100:.1f}%) | range [{lower:.1f}, {upper:.1f}]")

# ==============================================================================
# 14. CLASS IMBALANCE DISCUSSION
# ==============================================================================
print("\n" + "=" * 80)
print("SECTION 14: CLASS IMBALANCE DISCUSSION")
print("=" * 80)

print(f"Churn rate: {train_df[TARGET_COLUMN].mean()*100:.2f}%")
print(f"Imbalance ratio: {imbalance_ratio:.1f}:1")
print("""
Assessment:
- ~15.7% churn rate = moderate imbalance (not extreme)
- Ratio ~5.4:1 is manageable
- Recommendations for modeling:
  1. Use stratified splits (already implemented)
  2. Consider class_weight='balanced' in models
  3. Use PR-AUC and F1 as primary metrics (not just accuracy)
  4. Accuracy baseline = ~84.3% (always predict majority class)
""")

# ==============================================================================
# 15. DUPLICATE ANALYSIS NOTE
# ==============================================================================
print("=" * 80)
print("SECTION 15: DUPLICATE ANALYSIS")
print("=" * 80)

print(f"Raw data: 3,150 rows with 300 exact duplicate rows (9.52%)")
print(f"After basic_cleaning(): {len(cleaned_df)} rows (duplicates removed)")
print(f"165 unique row patterns appeared more than once")
print(f"Churn rate in duplicated rows ({raw_df[raw_df.duplicated(keep=False)]['Churn'].mean():.4f}) is similar to non-duplicated ({raw_df[~raw_df.duplicated(keep=False)]['Churn'].mean():.4f})")
print(f"Duplicates appear to be data collection artifact, not leakage")

# ==============================================================================
# SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("EDA COMPLETE")
print("=" * 80)
print(f"Train shape: {train_df.shape}")
print(f"Figures saved to: reports/figures/")
print(f"Figures: target_distribution.png, correlation_matrix.png, status_vs_churn.png, customer_value_distribution.png, customer_value_vs_churn.png")
