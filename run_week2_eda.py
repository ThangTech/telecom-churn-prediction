"""
Week 2 EDA - Iranian Churn Dataset
Train set only - No test set contamination
"""
import sys
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Import from src
from src.data import (
    load_raw_data,
    basic_cleaning,
    build_train_validation_split,
    TARGET_COLUMN
)

print("=" * 80)
print("WEEK 2 EDA - IRANIAN CHURN DATASET")
print("=" * 80)

# ==============================================================================
# 1. LOAD AND SPLIT DATA
# ==============================================================================
print("\n" + "=" * 80)
print("1. LOADING AND SPLITTING DATA")
print("=" * 80)

raw_df = load_raw_data('data/raw/Customer Churn.csv')
print(f"Raw data loaded: {raw_df.shape}")

cleaned_df = basic_cleaning(raw_df)
print(f"After cleaning: {cleaned_df.shape}")

# Split data - TRAIN/VAL/TEST
train_df, val_df, test_df = build_train_validation_split(
    cleaned_df, 
    target_col=TARGET_COLUMN,
    test_size=0.2,
    val_size=0.25,
    random_state=42
)

print(f"\nSplit Results:")
print(f"  Train: {train_df.shape} ({len(train_df)/len(cleaned_df)*100:.1f}%)")
print(f"  Val:   {val_df.shape} ({len(val_df)/len(cleaned_df)*100:.1f}%)")
print(f"  Test:  {test_df.shape} ({len(test_df)/len(cleaned_df)*100:.1f}%)")

# Verify stratification
print(f"\nTarget Distribution (stratification check):")
print(f"  Full:  {cleaned_df[TARGET_COLUMN].value_counts(normalize=True).sort_index().to_dict()}")
print(f"  Train: {train_df[TARGET_COLUMN].value_counts(normalize=True).sort_index().to_dict()}")
print(f"  Val:   {val_df[TARGET_COLUMN].value_counts(normalize=True).sort_index().to_dict()}")
print(f"  Test:  {test_df[TARGET_COLUMN].value_counts(normalize=True).sort_index().to_dict()}")

print("\n✓ Split verified - using TRAIN ONLY for EDA")

# ==============================================================================
# 2. TRAIN SET OVERVIEW
# ==============================================================================
print("\n" + "=" * 80)
print("2. TRAIN SET OVERVIEW")
print("=" * 80)

print(f"\nShape: {train_df.shape}")
print(f"Rows: {train_df.shape[0]:,}")
print(f"Columns: {train_df.shape[1]}")

print(f"\nColumns:")
for i, col in enumerate(train_df.columns, 1):
    print(f"  {i:2d}. {col}")

print(f"\nData Types:")
print(train_df.dtypes)

print(f"\nMemory Usage:")
print(f"{train_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# ==============================================================================
# 3. TARGET DISTRIBUTION
# ==============================================================================
print("\n" + "=" * 80)
print("3. TARGET DISTRIBUTION (TRAIN)")
print("=" * 80)

target_counts = train_df[TARGET_COLUMN].value_counts().sort_index()
target_pct = train_df[TARGET_COLUMN].value_counts(normalize=True).sort_index()

print(f"\nChurn Distribution:")
for val in sorted(target_counts.index):
    count = target_counts[val]
    pct = target_pct[val] * 100
    label = "No Churn" if val == 0 else "Churn"
    print(f"  {val} ({label}): {count:,} ({pct:.2f}%)")

churn_rate = target_pct[1] * 100
print(f"\nChurn Rate: {churn_rate:.2f}%")
print(f"Class Imbalance Ratio: {target_counts[0]/target_counts[1]:.2f}:1")

# ==============================================================================
# 4. DESCRIPTIVE STATISTICS
# ==============================================================================
print("\n" + "=" * 80)
print("4. DESCRIPTIVE STATISTICS (NUMERIC FEATURES)")
print("=" * 80)

numeric_cols = train_df.select_dtypes(include=[np.number]).columns.tolist()
if TARGET_COLUMN in numeric_cols:
    numeric_cols.remove(TARGET_COLUMN)

print(f"\nNumeric features: {len(numeric_cols)}")
print("\nDescriptive Statistics:")
print(train_df[numeric_cols].describe().T.to_string())

# ==============================================================================
# 5. MISSING VALUES
# ==============================================================================
print("\n" + "=" * 80)
print("5. MISSING VALUES (TRAIN)")
print("=" * 80)

missing = train_df.isnull().sum()
missing_pct = (missing / len(train_df)) * 100
missing_df = pd.DataFrame({
    'Column': missing.index,
    'Missing': missing.values,
    'Percentage': missing_pct.values
})
missing_df = missing_df[missing_df['Missing'] > 0]

if len(missing_df) > 0:
    print(f"\n⚠ Found {len(missing_df)} columns with missing values:")
    print(missing_df.to_string(index=False))
else:
    print("\n✓ No missing values in train set")

# ==============================================================================
# 6. DUPLICATES
# ==============================================================================
print("\n" + "=" * 80)
print("6. DUPLICATE ROWS (TRAIN)")
print("=" * 80)

n_dup = train_df.duplicated().sum()
print(f"\nDuplicate rows: {n_dup:,}")
if n_dup > 0:
    print(f"Percentage: {n_dup/len(train_df)*100:.2f}%")
else:
    print("✓ No duplicates in train set")

# ==============================================================================
# 7. OUTLIERS
# ==============================================================================
print("\n" + "=" * 80)
print("7. OUTLIER DETECTION (IQR METHOD)")
print("=" * 80)

outlier_summary = []
for col in numeric_cols:
    Q1 = train_df[col].quantile(0.25)
    Q3 = train_df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    outliers = train_df[(train_df[col] < lower) | (train_df[col] > upper)]
    n_outliers = len(outliers)
    pct_outliers = n_outliers / len(train_df) * 100
    
    outlier_summary.append({
        'Feature': col,
        'Outliers': n_outliers,
        'Percentage': f'{pct_outliers:.2f}%',
        'Lower_Bound': f'{lower:.2f}',
        'Upper_Bound': f'{upper:.2f}'
    })

outlier_df = pd.DataFrame(outlier_summary)
outlier_df = outlier_df[outlier_df['Outliers'] > 0]

if len(outlier_df) > 0:
    print(f"\nFeatures with outliers:")
    print(outlier_df.to_string(index=False))
else:
    print("\n✓ No outliers detected")

# ==============================================================================
# 8. CORRELATION MATRIX
# ==============================================================================
print("\n" + "=" * 80)
print("8. CORRELATION ANALYSIS")
print("=" * 80)

# All numeric features including target
numeric_with_target = numeric_cols + [TARGET_COLUMN]
corr_matrix = train_df[numeric_with_target].corr()

print(f"\nCorrelation with Target (Churn):")
target_corr = corr_matrix[TARGET_COLUMN].drop(TARGET_COLUMN).sort_values(ascending=False)
for feat, corr_val in target_corr.items():
    print(f"  {feat:<30} {corr_val:>7.4f}")

# ==============================================================================
# 9. STATUS vs CHURN ANALYSIS (CRITICAL)
# ==============================================================================
print("\n" + "=" * 80)
print("9. STATUS vs CHURN ANALYSIS (LEAKAGE CHECK)")
print("=" * 80)

if 'Status' in train_df.columns:
    print("\nStatus Distribution:")
    status_counts = train_df['Status'].value_counts().sort_index()
    for val, count in status_counts.items():
        pct = count / len(train_df) * 100
        print(f"  Status {val}: {count:,} ({pct:.2f}%)")
    
    print("\nStatus vs Churn Cross-tabulation:")
    crosstab = pd.crosstab(train_df['Status'], train_df[TARGET_COLUMN], normalize='index')
    print(crosstab)
    
    print("\nChurn Rate by Status:")
    churn_by_status = train_df.groupby('Status')[TARGET_COLUMN].agg(['sum', 'count', 'mean'])
    churn_by_status.columns = ['Churned', 'Total', 'Churn_Rate']
    churn_by_status['Churn_Rate_Pct'] = churn_by_status['Churn_Rate'] * 100
    print(churn_by_status)
    
    # Correlation
    status_churn_corr = train_df[['Status', TARGET_COLUMN]].corr().iloc[0, 1]
    print(f"\nCorrelation (Status, Churn): {status_churn_corr:.4f}")
    
    # Decision
    max_churn_rate = churn_by_status['Churn_Rate'].max()
    print(f"\n{'='*60}")
    print("STATUS LEAKAGE ASSESSMENT:")
    print(f"{'='*60}")
    print(f"Max churn rate in any Status: {max_churn_rate*100:.2f}%")
    print(f"Correlation with Churn: {abs(status_churn_corr):.4f}")
    
    if max_churn_rate > 0.8:
        print("🔴 HIGH LEAKAGE RISK: Status shows >80% churn rate")
        print("RECOMMENDATION: DROP Status column")
    elif abs(status_churn_corr) > 0.7:
        print("🟡 MEDIUM LEAKAGE RISK: High correlation with Churn")
        print("RECOMMENDATION: Investigate further or DROP")
    else:
        print("✓ LOW LEAKAGE RISK: Status appears safe to use")
        print("RECOMMENDATION: Keep Status as feature")
else:
    print("\n⚠ Status column not found")

# ==============================================================================
# 10. CUSTOMER VALUE ANALYSIS (CRITICAL)
# ==============================================================================
print("\n" + "=" * 80)
print("10. CUSTOMER VALUE ANALYSIS (ID CHECK)")
print("=" * 80)

if 'Customer Value' in train_df.columns:
    cv_col = 'Customer Value'
    
    print(f"\nCustomer Value Statistics:")
    print(train_df[cv_col].describe())
    
    print(f"\nUniqueness:")
    n_unique = train_df[cv_col].nunique()
    uniqueness = n_unique / len(train_df) * 100
    print(f"  Unique values: {n_unique:,} / {len(train_df):,}")
    print(f"  Uniqueness: {uniqueness:.2f}%")
    
    # Check if sequential (ID-like)
    sorted_vals = train_df[cv_col].sort_values().values[:20]
    print(f"\nFirst 20 sorted values:")
    print(sorted_vals)
    
    # Distribution
    print(f"\nDistribution:")
    print(f"  Min: {train_df[cv_col].min():.2f}")
    print(f"  Q1:  {train_df[cv_col].quantile(0.25):.2f}")
    print(f"  Median: {train_df[cv_col].median():.2f}")
    print(f"  Q3:  {train_df[cv_col].quantile(0.75):.2f}")
    print(f"  Max: {train_df[cv_col].max():.2f}")
    print(f"  Std: {train_df[cv_col].std():.2f}")
    
    # Relationship with Churn
    print(f"\nCustomer Value by Churn:")
    cv_by_churn = train_df.groupby(TARGET_COLUMN)[cv_col].describe()
    print(cv_by_churn)
    
    # Correlation
    cv_churn_corr = train_df[[cv_col, TARGET_COLUMN]].corr().iloc[0, 1]
    print(f"\nCorrelation (Customer Value, Churn): {cv_churn_corr:.4f}")
    
    # Decision
    print(f"\n{'='*60}")
    print("CUSTOMER VALUE ASSESSMENT:")
    print(f"{'='*60}")
    print(f"Uniqueness: {uniqueness:.2f}%")
    print(f"Correlation with Churn: {abs(cv_churn_corr):.4f}")
    
    if uniqueness > 99.5:
        print("🟡 HIGH UNIQUENESS: Likely a customer ID or unique identifier")
        print("RECOMMENDATION: Consider dropping unless verified as valid feature")
    elif abs(cv_churn_corr) < 0.05:
        print("⚠ LOW PREDICTIVE POWER: Weak relationship with Churn")
        print("RECOMMENDATION: May not be useful for modeling")
    else:
        print("✓ APPEARS VALID: Reasonable uniqueness and predictive signal")
        print("RECOMMENDATION: Keep Customer Value as feature")
else:
    print("\n⚠ Customer Value column not found")

# ==============================================================================
# 11. CATEGORICAL FEATURES
# ==============================================================================
print("\n" + "=" * 80)
print("11. CATEGORICAL FEATURES ANALYSIS")
print("=" * 80)

categorical_cols = ['Age Group', 'Tariff Plan', 'Status']
categorical_cols = [c for c in categorical_cols if c in train_df.columns]

for col in categorical_cols:
    print(f"\n{col}:")
    value_counts = train_df[col].value_counts().sort_index()
    for val, count in value_counts.items():
        pct = count / len(train_df) * 100
        print(f"  {val}: {count:,} ({pct:.2f}%)")
    
    # Churn rate by category
    churn_rate_by_cat = train_df.groupby(col)[TARGET_COLUMN].mean() * 100
    print(f"  Churn rate by {col}:")
    for val, rate in churn_rate_by_cat.items():
        print(f"    {val}: {rate:.2f}%")

# ==============================================================================
# 12. CLASS IMBALANCE
# ==============================================================================
print("\n" + "=" * 80)
print("12. CLASS IMBALANCE SUMMARY")
print("=" * 80)

minority_size = target_counts[1]
majority_size = target_counts[0]
imbalance_ratio = majority_size / minority_size

print(f"\nMinority class (Churn=1): {minority_size:,} samples")
print(f"Majority class (Churn=0): {majority_size:,} samples")
print(f"Imbalance ratio: {imbalance_ratio:.2f}:1")

if imbalance_ratio > 10:
    severity = "SEVERE"
elif imbalance_ratio > 5:
    severity = "MODERATE"
else:
    severity = "MILD"

print(f"Imbalance severity: {severity}")
print(f"\nRecommendation: Use stratified sampling ✓")
print(f"Consider class_weight='balanced' for Logistic Regression")

# ==============================================================================
# 13. SCALE DIFFERENCES
# ==============================================================================
print("\n" + "=" * 80)
print("13. FEATURE SCALE ANALYSIS")
print("=" * 80)

print(f"\nFeature Scales (mean ± std):")
for col in numeric_cols:
    mean = train_df[col].mean()
    std = train_df[col].std()
    min_val = train_df[col].min()
    max_val = train_df[col].max()
    print(f"  {col:<30} {mean:>10.2f} ± {std:>10.2f}  [{min_val:>8.1f}, {max_val:>10.1f}]")

print(f"\n✓ Features have different scales")
print(f"RECOMMENDATION: Use StandardScaler for Logistic Regression")

# ==============================================================================
# 14. SAVE EDA VISUALIZATIONS
# ==============================================================================
print("\n" + "=" * 80)
print("14. GENERATING EDA VISUALIZATIONS")
print("=" * 80)

output_dir = Path('reports/figures')
output_dir.mkdir(parents=True, exist_ok=True)

# Plot 1: Target distribution
plt.figure(figsize=(8, 5))
target_counts.plot(kind='bar', color=['#2ecc71', '#e74c3c'])
plt.title('Target Distribution (Train Set)', fontsize=14, fontweight='bold')
plt.xlabel('Churn', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks([0, 1], ['No Churn (0)', 'Churn (1)'], rotation=0)
for i, v in enumerate(target_counts.values):
    plt.text(i, v + 20, f'{v:,}\n({target_pct.values[i]*100:.1f}%)', 
             ha='center', fontsize=10)
plt.tight_layout()
plt.savefig(output_dir / 'target_distribution.png', dpi=200)
plt.close()
print("✓ Saved: target_distribution.png")

# Plot 2: Correlation matrix
plt.figure(figsize=(14, 12))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix (Train Set)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / 'correlation_matrix.png', dpi=200)
plt.close()
print("✓ Saved: correlation_matrix.png")

# Plot 3: Status vs Churn
if 'Status' in train_df.columns:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Distribution
    status_counts.plot(kind='bar', ax=ax1, color='steelblue')
    ax1.set_title('Status Distribution', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Status')
    ax1.set_ylabel('Count')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
    
    # Churn rate
    churn_by_status['Churn_Rate_Pct'].plot(kind='bar', ax=ax2, color='coral')
    ax2.set_title('Churn Rate by Status', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Status')
    ax2.set_ylabel('Churn Rate (%)')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
    ax2.axhline(churn_rate, color='red', linestyle='--', label=f'Overall: {churn_rate:.1f}%')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'status_vs_churn.png', dpi=200)
    plt.close()
    print("✓ Saved: status_vs_churn.png")

# Plot 4: Customer Value distribution
if 'Customer Value' in train_df.columns:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Overall distribution
    train_df[cv_col].hist(bins=50, ax=ax1, color='skyblue', edgecolor='black')
    ax1.set_title('Customer Value Distribution', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Customer Value')
    ax1.set_ylabel('Frequency')
    
    # By Churn
    train_df[train_df[TARGET_COLUMN]==0][cv_col].hist(bins=30, ax=ax2, alpha=0.5, 
                                                        label='No Churn', color='green')
    train_df[train_df[TARGET_COLUMN]==1][cv_col].hist(bins=30, ax=ax2, alpha=0.5, 
                                                        label='Churn', color='red')
    ax2.set_title('Customer Value by Churn', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Customer Value')
    ax2.set_ylabel('Frequency')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'customer_value_distribution.png', dpi=200)
    plt.close()
    print("✓ Saved: customer_value_distribution.png")

# Plot 5: Feature distributions (top numeric features by correlation)
top_features = target_corr.abs().nlargest(6).index.tolist()
if len(top_features) > 0:
    n_feats = len(top_features)
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()
    
    for idx, feat in enumerate(top_features):
        train_df[feat].hist(bins=30, ax=axes[idx], color='lightblue', edgecolor='black')
        axes[idx].set_title(f'{feat}\n(corr: {target_corr[feat]:.3f})', fontsize=10)
        axes[idx].set_ylabel('Frequency')
    
    # Hide unused subplots
    for idx in range(len(top_features), len(axes)):
        axes[idx].axis('off')
    
    plt.suptitle('Top Features by Correlation with Churn', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'feature_distributions.png', dpi=200)
    plt.close()
    print("✓ Saved: feature_distributions.png")

print(f"\nAll visualizations saved to: {output_dir}")

# ==============================================================================
# 15. SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("15. EDA SUMMARY")
print("=" * 80)

print(f"""
TRAIN SET EDA COMPLETE

Dataset:
- Train shape: {train_df.shape}
- Features: {len(numeric_cols)} numeric
- Target: {TARGET_COLUMN} (churn rate: {churn_rate:.2f}%)

Quality:
- Missing values: {missing.sum()}
- Duplicates: {n_dup}
- Class imbalance: {imbalance_ratio:.2f}:1 ({severity})

Critical Findings:
- Status column: {('Investigated - see Section 9' if 'Status' in train_df.columns else 'Not found')}
- Customer Value: {('Investigated - see Section 10' if 'Customer Value' in train_df.columns else 'Not found')}

Visualizations: {len(list(output_dir.glob('*.png')))} plots saved

Next Steps:
1. Review Status and Customer Value decisions
2. Update documentation with findings
3. Proceed to preprocessing and baseline modeling
""")

print("=" * 80)
print("WEEK 2 EDA COMPLETED")
print("=" * 80)
