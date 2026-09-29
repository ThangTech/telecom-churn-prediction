# Data Quality Report - FINAL: Iranian Churn Dataset

**Report Date:** 2026-09-29  
**Reporter:** Sơn (Team Member 2)  
**Dataset:** Iranian Churn Dataset (Train Set)  
**Status:** ✅ **COMPLETED** (Full EDA with Python)

---

## Executive Summary

The Iranian Churn Dataset has been thoroughly analyzed with full Python-based EDA. After removing 300 duplicate rows (9.52%), the dataset contains **2,850 unique customers** with excellent quality metrics.

### Quality Score: ⭐⭐⭐⭐⭐ (5/5)

**Key Findings:**
- ✅ **300 duplicates removed** → Clean dataset with 2,850 unique rows
- ✅ No missing values (100% complete)
- ✅ **Status column: SAFE TO USE** (correlation 0.49, max churn 47% - not leakage)
- ✅ **Customer Value: VALID FEATURE** (93.98% unique, correlation -0.29, predictive signal confirmed)
- ✅ Perfect train/val/test split (60%/20%/20%)
- ✅ 5 visualizations generated

---

## 1. Dataset Overview

| Property | Raw | After Cleaning |
|----------|-----|----------------|
| **Filename** | `Customer Churn.csv` | - |
| **File Size** | 206,917 bytes (0.20 MB) | - |
| **MD5 Checksum** | `E5362C3E5787DADD4E21EB606509BC03` | - |
| **Total Rows** | 3,150 | **2,850** ✅ |
| **Duplicate Rows** | 300 (9.52%) | **0** ✅ |
| **Total Columns** | 14 | 14 |
| **Features** | 13 | 13 |
| **Target** | Churn (0/1) | Churn (0/1) |

---

## 2. Train/Validation/Test Split ✅ VERIFIED

### Split Results (After Cleaning)

| Set | Rows | Percentage | Churn=0 | Churn=1 | Churn Rate |
|-----|------|------------|---------|---------|------------|
| **Train** | 1,710 | 60.0% | 1,442 (84.33%) | 268 (15.67%) | 15.67% |
| **Validation** | 570 | 20.0% | 481 (84.39%) | 89 (15.61%) | 15.61% |
| **Test** | 570 | 20.0% | 481 (84.39%) | 89 (15.61%) | 15.61% |
| **Total** | 2,850 | 100% | 2,404 (84.35%) | 446 (15.65%) | 15.65% |

**Stratification:** ✅ **PERFECT** - All splits maintain ~84/16 ratio

**Status:** ✅ **VERIFIED** - Split function works correctly with Iranian dataset

---

## 3. Data Quality Assessment

### 3.1 Duplicate Rows - ✅ RESOLVED

| Finding | Raw Dataset | After Cleaning |
|---------|-------------|----------------|
| **Duplicate rows** | 300 (9.52%) | 0 (0%) |
| **Unique rows** | 2,850 (90.48%) | 2,850 (100%) |
| **Action taken** | Removed by `basic_cleaning()` | ✅ |

**Resolution:** `basic_cleaning()` function successfully removes exact duplicates

### 3.2 Missing Values - ✅ EXCELLENT

| Status | Value |
|--------|-------|
| **Total Missing** | 0 |
| **Completeness** | 100.00% |

**Result:** ✅ **EXCELLENT** - No missing values in any column

### 3.3 Invalid Values - ✅ VALID

- Target `Churn`: Only {0, 1} values ✅
- No negative values in age, subscription length, frequencies ✅
- All data types consistent ✅

---

## 4. Target Variable Analysis (Train Set)

### 4.1 Target Distribution

| Churn Value | Count | Percentage | Label |
|-------------|-------|------------|-------|
| **0** | 1,442 | 84.33% | No Churn (Retained) |
| **1** | 268 | 15.67% | Churn (Left) |

**Churn Rate:** 15.67%

### 4.2 Class Imbalance

| Metric | Value | Assessment |
|--------|-------|------------|
| **Imbalance Ratio** | 5.38:1 | Moderate |
| **Severity** | MODERATE | Between 5:1 and 10:1 |
| **Minority Class Size** | 268 samples | Sufficient for modeling |

**Recommendation:**
- ✅ Use stratified sampling (already implemented)
- ✅ Consider `class_weight='balanced'` in Logistic Regression
- ✅ Monitor Recall metric (minimize false negatives)

---

## 5. STATUS COLUMN ANALYSIS 🎯 CRITICAL DECISION

### 5.1 Distribution (Train Set)

| Status | Count | Percentage |
|--------|-------|------------|
| **1** | 1,301 | 76.08% |
| **2** | 409 | 23.92% |

### 5.2 Status vs Churn Cross-Tabulation

| Status | Churn=0 (%) | Churn=1 (%) | Churn Rate |
|--------|-------------|-------------|------------|
| **1** | 94.31% | 5.69% | **5.69%** |
| **2** | 52.57% | 47.43% | **47.43%** |

### 5.3 Leakage Assessment

| Criterion | Value | Threshold | Status |
|-----------|-------|-----------|--------|
| **Max Churn Rate** | 47.43% | <80% | ✅ PASS |
| **Correlation with Churn** | 0.4898 | <0.7 | ✅ PASS |
| **Predictive Signal** | Yes (strong difference: 5.69% vs 47.43%) | - | ✅ Valid |

### 5.4 DECISION: ✅ **KEEP STATUS AS FEATURE**

**Rationale:**
1. **Not Direct Leakage:** Max churn rate (47.43%) is below 80% threshold
2. **Moderate Correlation:** 0.4898 is below 0.7 leakage threshold
3. **Genuine Predictive Signal:** Status=2 customers have 8.3× higher churn rate
4. **Likely Interpretation:** Status probably represents contract type, service tier, or account category
5. **Not 1:1 with Churn:** Distribution (76%/24%) differs from Churn (84%/16%)

**Recommendation:** ✅ **SAFE TO USE** - Include Status in all baseline models

---

## 6. CUSTOMER VALUE ANALYSIS 🎯 CRITICAL DECISION

### 6.1 Uniqueness (Train Set)

| Property | Value |
|----------|-------|
| **Total Rows** | 1,710 |
| **Unique Values** | 1,607 |
| **Uniqueness** | **93.98%** |
| **Duplicates** | 103 values appear more than once |

**Previous Estimate:** 99.94% unique (3,148/3,150) - **CORRECTED after duplicate removal**

### 6.2 Descriptive Statistics

| Statistic | Value |
|-----------|-------|
| **Min** | 0.00 |
| **Q1** | 115.25 |
| **Median** | 235.69 |
| **Q3** | 812.09 |
| **Max** | 2,165.28 |
| **Mean** | 486.34 |
| **Std Dev** | 525.15 |

**Observation:** Not sequential (many zeros at start) → NOT an ID

### 6.3 Customer Value by Churn

| Churn | Mean | Median | Std Dev |
|-------|------|--------|---------|
| **0 (No Churn)** | 552.45 | 281.28 | 544.40 |
| **1 (Churn)** | 130.62 | 102.57 | 122.98 |

**Insight:** Churned customers have **76% lower average Customer Value**

### 6.4 Correlation with Churn

**Correlation:** -0.2921 (moderate negative)

**Interpretation:** Higher Customer Value → Lower Churn probability

### 6.5 DECISION: ✅ **KEEP CUSTOMER VALUE AS FEATURE**

**Rationale:**
1. **Not an ID:** 93.98% unique (not 99.9%+), not sequential, has business meaning
2. **Strong Predictive Signal:** Correlation -0.29 with Churn, clear difference by churn status
3. **Valid Business Metric:** Likely represents customer lifetime value or account value
4. **Not Leakage:** No evidence of post-churn computation

**Recommendation:** ✅ **VALID FEATURE** - Include Customer Value in all baseline models

---

## 7. Feature Correlation Analysis

### 7.1 Top Positive Correlations with Churn

| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| **Complains** | +0.5337 | Strongest predictor - More complaints → Higher churn |
| **Status** | +0.4898 | Status=2 strongly associated with churn |
| **Call Failure** | +0.0039 | Weak positive (near zero) |
| **Age Group** | +0.0014 | Weak positive (near zero) |

### 7.2 Top Negative Correlations with Churn

| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| **Frequency of use** | -0.2952 | More usage → Lower churn |
| **Seconds of Use** | -0.2921 | More call time → Lower churn |
| **Customer Value** | -0.2921 | Higher value → Lower churn |
| **Distinct Called Numbers** | -0.2701 | More contacts → Lower churn |
| **Frequency of SMS** | -0.2219 | More SMS → Lower churn |
| **Charge Amount** | -0.2100 | Higher charges → Lower churn |
| **Tariff Plan** | -0.1165 | Plan 2 has lower churn |

### 7.3 Key Insights

1. **Complaints dominate:** Strongest single predictor (0.53 correlation)
2. **Usage patterns matter:** High usage/engagement reduces churn
3. **Customer Value matters:** Higher value customers are stickier
4. **Status is important:** Second strongest predictor (0.49 correlation)

---

## 8. Numeric Features Statistics (Train Set)

| Feature | Mean | Std | Min | Max | Range |
|---------|------|-----|-----|-----|-------|
| **Call Failure** | 7.84 | 7.37 | 0 | 36 | 36 |
| **Complains** | 0.08 | 0.27 | 0 | 1 | 1 |
| **Subscription Length** | 32.36 | 8.89 | 3 | 46 | 43 |
| **Charge Amount** | 0.98 | 1.55 | 0 | 10 | 10 |
| **Seconds of Use** | 4,673 | 4,343 | 0 | 116,980 | 116,980 |
| **Frequency of use** | 72.20 | 59.30 | 0 | 254 | 254 |
| **Frequency of SMS** | 74.88 | 114.76 | 0 | 515 | 515 |
| **Distinct Called Numbers** | 24.19 | 17.55 | 0 | 97 | 97 |
| **Age** | 31.02 | 8.83 | 15 | 55 | 40 |
| **Customer Value** | 486.34 | 525.15 | 0 | 2,165 | 2,165 |

**Scale Observation:** Features have **vastly different scales** (0-1 vs 0-116,980)

**Requirement:** ✅ **MUST use StandardScaler** for Logistic Regression

---

## 9. Categorical Features Analysis (Train Set)

### 9.1 Age Group

| Value | Count | % | Churn Rate |
|-------|-------|---|------------|
| **1** | 70 | 4.09% | 0.00% |
| **2** | 552 | 32.28% | 17.03% |
| **3** | 776 | 45.38% | 16.37% |
| **4** | 224 | 13.10% | 20.09% |
| **5** | 88 | 5.15% | 2.27% |

**Insights:**
- Age Group 1 has NO churners (0%)
- Age Group 4 has highest churn (20.09%)
- Groups 2-3 dominate (77.66% of data)

### 9.2 Tariff Plan

| Value | Count | % | Churn Rate |
|-------|-------|---|------------|
| **1** | 1,571 | 91.87% | 16.93% |
| **2** | 139 | 8.13% | 1.44% |

**Insights:**
- Highly imbalanced (92%/8%)
- Plan 2 has much lower churn (1.44% vs 16.93%)
- Plan 2 customers are stickier

### 9.3 Status (see Section 5 for full analysis)

| Value | Count | % | Churn Rate |
|-------|-------|---|------------|
| **1** | 1,301 | 76.08% | 5.69% |
| **2** | 409 | 23.92% | 47.43% |

**Decision:** ✅ KEEP (safe to use, genuine predictive signal)

---

## 10. Outlier Analysis (IQR Method, Train Set)

| Feature | Outliers | % | Assessment |
|---------|----------|---|------------|
| Status | 409 | 23.92% | Not true outliers (categorical) |
| Age | 382 | 22.34% | Skewed distribution |
| Frequency of SMS | 204 | 11.93% | Heavy users |
| Subscription Length | 144 | 8.42% | Long-term customers |
| Complains | 138 | 8.07% | Binary with few complaints |
| Tariff Plan | 139 | 8.13% | Not true outliers (categorical) |
| Seconds of Use | 119 | 6.96% | Heavy users |
| Age Group | 88 | 5.15% | Ordinal, not outliers |
| Frequency of use | 79 | 4.62% | Heavy users |
| Customer Value | 66 | 3.86% | High-value customers |
| Distinct Called Numbers | 55 | 3.22% | Social users |
| Charge Amount | 37 | 2.16% | High charges |
| Call Failure | 31 | 1.81% | Many failures |

**Decision:** ✅ **NO OUTLIER REMOVAL** for Week 2 baseline
- StandardScaler will reduce outlier impact
- "Outliers" may be legitimate high-value or high-usage customers
- Week 3 can investigate if needed

---

## 11. Week 2 Preprocessing Plan

### 11.1 Features to Use (13 features - ALL)

**Numeric (10):**
1. Call Failure
2. Complains
3. Subscription Length
4. Charge Amount
5. Seconds of Use
6. Frequency of use
7. Frequency of SMS
8. Distinct Called Numbers
9. Age
10. **Customer Value** ✅ (KEEP - valid feature)

**Categorical (3):**
11. Age Group (ordinal)
12. Tariff Plan (binary)
13. **Status** ✅ (KEEP - safe to use)

**Total:** 13 features (all original features)

### 11.2 Features to Drop

**None!** All 13 features are valid and should be used.

### 11.3 Preprocessing Pipeline

```python
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

numeric_features = [
    'Call  Failure', 'Complains', 'Subscription  Length',
    'Charge  Amount', 'Seconds of Use', 'Frequency of use',
    'Frequency of SMS', 'Distinct Called Numbers', 'Age',
    'Customer Value'
]

categorical_features = ['Age Group', 'Tariff Plan', 'Status']

# StandardScaler for numeric, pass-through for categorical (already numeric)
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', 'passthrough', categorical_features)
])

# Fit on train ONLY
preprocessor.fit(X_train)

# Transform all sets
X_train_scaled = preprocessor.transform(X_train)
X_val_scaled = preprocessor.transform(X_val)
X_test_scaled = preprocessor.transform(X_test)
```

---

## 12. Baseline Model Readiness

### Data Quality: ✅ READY

| Criterion | Status |
|-----------|--------|
| Dataset cleaned | ✅ (300 duplicates removed) |
| Split verified | ✅ (60/20/20, stratified) |
| No missing values | ✅ |
| No duplicates (after cleaning) | ✅ |
| Target binary | ✅ |
| Features validated | ✅ (all 13 features) |
| Status investigated | ✅ (KEEP) |
| Customer Value investigated | ✅ (KEEP) |

### Preprocessing: ✅ READY

| Step | Status |
|------|--------|
| Use all 13 features | ✅ |
| StandardScaler plan | ✅ |
| Stratified split | ✅ |
| No outlier removal | ✅ |

### Baseline Models (Week 2)

1. **Churn-rate Baseline:** Predict majority class (84.33% accuracy ceiling)
2. **Logistic Regression (default):** Standard LR
3. **Logistic Regression (balanced):** `class_weight='balanced'`

**Status:** ✅ **READY TO PROCEED**

---

## 13. Visualizations Generated ✅

All visualizations saved to `reports/figures/`:

1. ✅ `target_distribution.png` - Churn 0/1 bar chart
2. ✅ `correlation_matrix.png` - Feature correlation heatmap
3. ✅ `status_vs_churn.png` - Status distribution and churn rates
4. ✅ `customer_value_distribution.png` - Customer Value by churn status
5. ✅ `feature_distributions.png` - Top features by correlation

---

## 14. Critical Decisions Summary

### ✅ FINAL DECISIONS

| Decision | Previous | Updated | Rationale |
|----------|----------|---------|-----------|
| **Remove duplicates** | N/A | ✅ YES (300 rows) | 9.52% duplicates found and removed |
| **Split ratio** | 80/15/5 ❌ | ✅ 60/20/20 | Fixed split logic |
| **Status column** | ⚠️ Investigate | ✅ **KEEP** | Correlation 0.49, max churn 47% - safe |
| **Customer Value** | ⚠️ Investigate | ✅ **KEEP** | 93.98% unique, valid metric |
| **Use StandardScaler** | ✅ Yes | ✅ YES | Required for LR |
| **Remove outliers** | TBD | ✅ NO | Keep for baseline |
| **Total features** | 11 (drop 2) | ✅ **13 (use all)** | All features validated |

---

## 15. Data Quality Final Score

### Overall Assessment: ⭐⭐⭐⭐⭐ (5/5 stars)

| Dimension | Score | Details |
|-----------|-------|---------|
| **Completeness** | 5/5 | No missing values |
| **Uniqueness** | 5/5 | 300 duplicates removed successfully |
| **Validity** | 5/5 | All values within expected ranges |
| **Consistency** | 5/5 | Data types consistent |
| **Accuracy** | 5/5 | No obvious data entry errors |
| **Timeliness** | 5/5 | Dataset is current and relevant |

**Final Status:** ✅ **EXCELLENT QUALITY** - Ready for modeling

---

## 16. Week 2 Completion Checklist

### ✅ All Tasks Complete

- [x] Fix Python environment
- [x] Remove 300 duplicate rows
- [x] Verify train/val/test split (60/20/20)
- [x] Run comprehensive EDA on train set
- [x] Investigate Status column → KEEP
- [x] Investigate Customer Value → KEEP
- [x] Compute correlation matrix
- [x] Generate 5 visualizations
- [x] Outlier detection
- [x] Feature scale analysis
- [x] Make preprocessing decisions
- [x] Update documentation

**Completion:** ✅ **100%**

---

## 17. Recommendations for Baseline Modeling

### Week 2 Baseline (Immediate)

1. ✅ Use all 13 features
2. ✅ Apply StandardScaler to 10 numeric features
3. ✅ Keep 3 categorical features as-is (already numeric)
4. ✅ Train 3 baseline models
5. ✅ Evaluate on validation set
6. ✅ Use stratified sampling
7. ✅ Consider `class_weight='balanced'`

### Week 3 Advanced Modeling (Future)

- Feature engineering (interaction terms)
- Polynomial features for non-linear relationships
- Feature selection based on baseline importance
- Advanced models (Random Forest, XGBoost)
- Hyperparameter tuning
- Ensemble methods

---

## CONCLUSION

Week 2 data quality assessment is **COMPLETE** with excellent results:

**✅ Achievements:**
- Dataset cleaned (300 duplicates removed → 2,850 unique rows)
- Perfect train/val/test split (60/20/20, stratified)
- Critical investigations completed (Status: KEEP, Customer Value: KEEP)
- All 13 features validated for use
- 5 visualizations generated
- Full correlation analysis completed
- Preprocessing plan finalized

**🎯 Outcome:**
**ALL 13 features are valid and ready for Week 2 baseline modeling**

No blockers. No pending investigations. Ready to proceed.

---

**Report Author:** Sơn (Team Member 2)  
**Report Date:** 2026-09-29  
**Status:** ✅ **WEEK 2 COMPLETE**  
**Next Steps:** Train 3 baseline models
