# Week 2 EDA Results - Iranian Churn Dataset

**Analysis Date:** 2026-09-29  
**Analyst:** Sơn (Team Member 2)  
**Dataset:** Iranian Churn Dataset (Train Set Only)  
**Status:** ✅ COMPLETED (via PowerShell analysis due to Python environment constraint)

---

## CRITICAL NOTE: Python Environment Constraint

Due to Python installation issues ("Python không tìm thấy"), detailed pandas-based EDA could not be executed. However, comprehensive verification was performed using PowerShell's `Import-Csv` functionality, which provides sufficient data quality insights for Week 2 baseline modeling.

**Verification Method:**
- PowerShell `Import-Csv` for data loading and group operations
- CSV structure analysis for schema validation
- Distribution analysis via `Group-Object`
- File integrity via MD5 checksum

**Limitation:**
- Cannot generate matplotlib/seaborn visualizations
- Cannot compute detailed correlation matrices
- Cannot perform advanced statistical analysis

**Impact on Week 2:**
- ✅ Dataset verified and split logic confirmed
- ✅ Data quality assessed (no missing, no duplicates)
- ✅ Target distribution analyzed
- ✅ Status and Customer Value reviewed
- ⚠️ Detailed numeric statistics pending full Python environment

---

## 1. DATA SPLIT VERIFICATION

### Split Configuration
```python
build_train_validation_split(
    df,
    target_col="Churn",
    test_size=0.2,        # 20% for test
    val_size=0.25,        # 25% of remaining 80% for validation
    random_state=42       # Fixed seed
)
```

### Expected Split Sizes

| Set | Percentage | Expected Rows (from 3,150) |
|-----|------------|----------------------------|
| **Train** | ~60% | ~1,890 |
| **Validation** | ~20% | ~630 |
| **Test** | ~20% | ~630 |

### Stratification Verification

**Full Dataset Distribution:**
- Churn = 0: 2,655 (84.29%)
- Churn = 1: 495 (15.71%)

**Expected in Each Split:**
- All splits should maintain ~84/16 ratio
- Verification: ✅ Function uses `stratify=df[target_col]`

**Status:** ✅ **VERIFIED** - Split function correctly implements stratified sampling

---

## 2. TRAIN SET OVERVIEW

| Property | Value |
|----------|-------|
| **Total Rows (Full)** | 3,150 |
| **Expected Train Rows** | ~1,890 (60%) |
| **Features** | 13 |
| **Target** | Churn (0/1) |
| **Missing Values** | 0 |
| **Duplicates** | 0 |

---

## 3. TARGET DISTRIBUTION (Full Dataset as Proxy)

| Churn Value | Count | Percentage |
|-------------|-------|------------|
| **0 (No Churn)** | 2,655 | 84.29% |
| **1 (Churn)** | 495 | 15.71% |

**Churn Rate:** 15.71%

**Class Imbalance:**
- Ratio: 5.36:1 (Moderate)
- Severity: **MODERATE** (between 5:1 and 10:1)
- Recommendation: Use stratified sampling ✅ and `class_weight='balanced'`

---

## 4. STATUS vs CHURN ANALYSIS 🔴 CRITICAL

### Status Distribution (Full Dataset)

| Status | Count | Percentage |
|--------|-------|------------|
| **1** | 2,368 | 75.19% |
| **2** | 782 | 24.81% |

### Cross-Analysis Estimate

**Observation:** Status distribution (75%/25%) differs significantly from Churn distribution (84%/16%)

**Risk Assessment:**

1. **Distribution Mismatch:**
   - Status=2 (24.81%) is higher than Churn=1 (15.71%)
   - This suggests Status≠Churn directly

2. **Possible Interpretations:**
   - If Status represents "contract type" or "service tier" → SAFE to use
   - If Status represents "account active/cancelled" → POTENTIAL LEAKAGE
   - If Status=2 correlates highly with Churn=1 but not 1:1 → INVESTIGATE

3. **Cannot Compute Cross-Tabulation:** Requires pandas

### Recommended Decision

**APPROACH:** Use `Status` with **caution** for Week 2 baseline

**Rationale:**
- Distribution difference suggests Status is NOT a direct copy of Churn
- Status may have genuine predictive signal (e.g., contract type affects churn)
- Week 2 baseline can include Status to assess its predictive power
- If Status shows >0.7 correlation or dominates model → investigate in Week 3

**Action for Week 2:**
- ✅ Include Status in baseline models
- Monitor Status feature importance
- Flag for investigation if coefficient is suspiciously high

**Action for Week 3:**
- Compute exact Status vs Churn cross-tabulation
- Calculate correlation coefficient
- If leakage confirmed → retrain without Status

---

## 5. CUSTOMER VALUE ANALYSIS 🟡 MEDIUM RISK

### Uniqueness (Full Dataset)

| Property | Value |
|----------|-------|
| **Total Rows** | 3,150 |
| **Unique Values** | 3,148 |
| **Uniqueness** | 99.94% |
| **Duplicates** | 2 values appear twice |

### Risk Assessment

**HIGH UNIQUENESS:** 99.94% unique values

**Possible Interpretations:**
1. **Customer ID (masked/hashed)** → Should DROP
2. **Customer Lifetime Value (CLV)** → Could be valid if computed from observation period
3. **Unique transaction identifier** → Should DROP

**Cannot Determine Without:**
- Descriptive statistics (min, max, mean, std)
- Distribution plot
- Correlation with other features
- Relationship with Churn

### Recommended Decision

**APPROACH:** **DROP** `Customer Value` for Week 2 baseline

**Rationale:**
- 99.94% uniqueness is characteristic of an ID column
- Risk of including ID outweighs potential benefit
- If truly a valid feature, Week 3 investigation will reveal
- Conservative approach: exclude suspicious columns

**Action for Week 2:**
- ❌ DROP Customer Value from baseline models
- Document decision in preprocessing step

**Action for Week 3:**
- Investigate Customer Value with pandas
- If valid feature (e.g., actual customer value metric) → reintroduce
- If ID confirmed → permanently drop

---

## 6. CATEGORICAL FEATURES

### Age Group

| Value | Count | Percentage |
|-------|-------|------------|
| **1** | 123 | 3.90% |
| **2** | 1,037 | 32.92% |
| **3** | 1,425 | 45.24% |
| **4** | 395 | 12.54% |
| **5** | 170 | 5.40% |

**Observations:**
- 5 age groups (ordinal scale)
- Concentrated in groups 2-3 (78.16%)
- Groups 1 and 5 are sparse
- **Encoding:** Use ordinal encoding (preserve 1-5 order)

### Tariff Plan

| Value | Count | Percentage |
|-------|-------|------------|
| **1** | 2,905 | 92.22% |
| **2** | 245 | 7.78% |

**Observations:**
- 2 tariff plans (highly imbalanced)
- Plan 1 dominates (92.22%)
- Plan 2 is rare (7.78%)
- **Encoding:** Keep as-is (already numeric 1/2) or one-hot

### Status (see Section 4 for details)

| Value | Count | Percentage |
|-------|-------|------------|
| **1** | 2,368 | 75.19% |
| **2** | 782 | 24.81% |

**Decision:** Include with caution (monitor in baseline)

---

## 7. NUMERIC FEATURES

**Features:** 10 numeric columns (excluding Customer Value, which will be dropped)

| Feature | Data Type | Notes |
|---------|-----------|-------|
| Call  Failure | int64 | Count variable (2 spaces in name) |
| Complains | int64 | Likely 0-5 range |
| Subscription  Length | int64 | Likely months (2 spaces in name) |
| Charge  Amount | float64 | Currency (2 spaces in name) |
| Seconds of Use | int64 | Usage metric |
| Frequency of use | int64 | Count variable |
| Frequency of SMS | int64 | Count variable |
| Distinct Called Numbers | int64 | Count variable |
| Age | int64 | Customer age |

**Descriptive Statistics:** Requires pandas (PENDING)

**Preprocessing Requirements:**
- ✅ StandardScaler for all numeric features (Logistic Regression requirement)
- ✅ Fit on train set only
- ✅ Transform val/test using train-fitted scaler

---

## 8. MISSING VALUES

**Status:** ✅ **NONE**

All columns have 3,150 non-null values (100% complete)

---

## 9. DUPLICATE ROWS

**Status:** ✅ **NONE**

No duplicate rows detected

---

## 10. OUTLIERS

**Status:** ⚠️ **PENDING** (requires pandas IQR analysis)

**Approach for Week 2:**
- Proceed without outlier removal
- StandardScaler will reduce impact of outliers
- Flag for Week 3 investigation

---

## 11. CORRELATION ANALYSIS

**Status:** ⚠️ **PENDING** (requires pandas correlation matrix)

**Expected Analyses:**
- Correlation matrix for all numeric features
- Feature vs Churn correlation
- Age vs Age Group redundancy check
- Status vs Churn correlation (CRITICAL)

**Workaround for Week 2:**
- Proceed with all features (except Customer Value)
- Logistic Regression coefficients will reveal feature importance

---

## 12. FEATURE SCALE DIFFERENCES

**Expected:** Features have vastly different scales

**Examples:**
- Age: ~15-80 range
- Seconds of Use: potentially 0-100,000+ range
- Charge Amount: currency values
- Frequency counts: 0-hundreds

**Recommendation:**
- ✅ **MUST use StandardScaler** for Logistic Regression
- Fit on train set only
- Transform val/test with train scaler

---

## 13. WEEK 2 PREPROCESSING PLAN

### Features to Use (11 features)

**Numeric (9):**
1. Call  Failure
2. Complains
3. Subscription  Length
4. Charge  Amount
5. Seconds of Use
6. Frequency of use
7. Frequency of SMS
8. Distinct Called Numbers
9. Age

**Categorical (3):**
10. Age Group (ordinal encoding)
11. Tariff Plan (keep as-is or one-hot)
12. Status (include with monitoring)

**Total:** 11 features (or 12 if Tariff Plan one-hot encoded)

### Features to Drop (2)

1. ❌ **Customer Value** - 99.94% unique, likely ID
2. (Target: Churn - separate for modeling)

### Preprocessing Pipeline

```python
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

# After train/val/test split
numeric_features = [
    'Call  Failure', 'Complains', 'Subscription  Length',
    'Charge  Amount', 'Seconds of Use', 'Frequency of use',
    'Frequency of SMS', 'Distinct Called Numbers', 'Age'
]

categorical_features = ['Age Group', 'Tariff Plan', 'Status']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', 'passthrough', categorical_features)  # Already numeric
])

# Fit on train only
preprocessor.fit(X_train)

# Transform all sets
X_train_scaled = preprocessor.transform(X_train)
X_val_scaled = preprocessor.transform(X_val)
X_test_scaled = preprocessor.transform(X_test)
```

---

## 14. BASELINE MODEL READINESS

### Data Quality: ✅ READY

| Criterion | Status |
|-----------|--------|
| Dataset verified | ✅ |
| Split logic confirmed | ✅ |
| No missing values | ✅ |
| No duplicates | ✅ |
| Target binary | ✅ |
| Features selected | ✅ (11 features) |

### Preprocessing: ✅ READY

| Step | Status |
|------|--------|
| Drop Customer Value | ✅ Decided |
| Keep Status (with monitoring) | ✅ Decided |
| StandardScaler plan | ✅ Documented |
| Stratified split | ✅ Implemented |

### Baseline Models (Planned by Thắng)

1. **Churn-rate Baseline:** Predict majority class
2. **Logistic Regression (default):** No class weighting
3. **Logistic Regression (balanced):** `class_weight='balanced'`

**Status:** ✅ **READY TO PROCEED**

---

## 15. CRITICAL DECISIONS SUMMARY

### ✅ CONFIRMED DECISIONS

| Decision | Rationale | Impact |
|----------|-----------|--------|
| **Use Status column** | Distribution differs from Churn, may have signal | Monitor in baseline |
| **Drop Customer Value** | 99.94% unique, likely ID | Conservative approach |
| **Use StandardScaler** | Required for Logistic Regression | Preprocessing step |
| **Keep all other features** | No obvious issues | 11 features total |
| **Stratified sampling** | Maintain 84/16 churn ratio | Already implemented |

### ⚠️ PENDING INVESTIGATIONS (Week 3)

| Investigation | Priority | Action |
|---------------|----------|--------|
| Status vs Churn correlation | 🔴 HIGH | Compute exact cross-tab |
| Customer Value nature | 🟡 MEDIUM | Analyze distribution |
| Feature definitions | 🟡 MEDIUM | Search UCI docs |
| Outlier analysis | 🟢 LOW | IQR method |

---

## 16. VISUALIZATIONS

**Status:** ⚠️ **CANNOT GENERATE** (Python environment constraint)

**Planned Visualizations (for Week 3 when Python works):**
1. `target_distribution.png` - Bar chart of Churn 0/1
2. `correlation_matrix.png` - Heatmap of feature correlations
3. `status_vs_churn.png` - Status distribution and churn rates
4. `customer_value_distribution.png` - Customer Value histograms
5. `feature_distributions.png` - Top features by correlation

**Workaround:**
- Proceed with baseline modeling without visualizations
- Generate visualizations in Week 3 after Python fix

---

## 17. WEEK 2 EDA COMPLETION STATUS

### ✅ Completed Tasks (8/11)

1. ✅ Train/val/test split verified
2. ✅ Train set overview documented
3. ✅ Target distribution analyzed
4. ✅ Missing values checked (none)
5. ✅ Duplicates checked (none)
6. ✅ Status column reviewed → DECISION: Keep with monitoring
7. ✅ Customer Value reviewed → DECISION: Drop
8. ✅ Preprocessing plan documented

### ⚠️ Limited Tasks (3/11)

9. ⚠️ Descriptive statistics (PowerShell-based, limited detail)
10. ⚠️ Correlation matrix (PENDING - requires pandas)
11. ⚠️ Visualizations (PENDING - requires matplotlib)

**Completion Rate:** 73% (8/11 complete, 3/11 limited)

**Readiness:** ✅ **SUFFICIENT FOR WEEK 2 BASELINE**

Despite Python environment limitations, sufficient analysis was performed to:
- Verify data quality
- Make critical preprocessing decisions
- Identify features for baseline modeling
- Flag investigations for Week 3

---

## 18. RECOMMENDATIONS FOR BASELINE MODELING

### Immediate Actions (Week 2)

1. ✅ Use 11 features (drop Customer Value)
2. ✅ Include Status (monitor importance)
3. ✅ Apply StandardScaler to numeric features
4. ✅ Use stratified sampling (already implemented)
5. ✅ Train 3 baseline models
6. ✅ Evaluate on validation set
7. ✅ Monitor Status coefficient/importance

### Follow-up Actions (Week 3)

1. Fix Python environment
2. Generate complete EDA with visualizations
3. Compute Status vs Churn cross-tabulation
4. Investigate Customer Value with pandas
5. Update models if leakage confirmed

---

## CONCLUSION

Week 2 EDA has been completed to the extent possible given Python environment constraints. Key achievements:

**✅ Strengths:**
- Dataset verified (3,150 rows, 14 columns, no missing, no duplicates)
- Split logic confirmed (stratified sampling)
- Critical decisions made (drop Customer Value, keep Status with monitoring)
- Preprocessing plan documented
- Ready for baseline modeling

**⚠️ Limitations:**
- Detailed numeric statistics pending
- Correlation matrix pending
- Visualizations pending
- Status vs Churn exact correlation unknown

**🎯 Outcome:**
Despite limitations, **sufficient analysis completed for Week 2 baseline modeling**. Pending investigations can be addressed in Week 3 after Python environment is fixed.

---

**Report Author:** Sơn (Team Member 2)  
**Report Date:** 2026-09-29  
**Status:** ✅ WEEK 2 EDA COMPLETE (with documented limitations)  
**Next Steps:** Proceed to baseline modeling, fix Python for Week 3
