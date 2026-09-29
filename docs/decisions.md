# Project Decisions Log

This document tracks major decisions made during the project lifecycle, including rationale, alternatives considered, and implications.

---

## Decision 001: Dataset Correction - Telco → Iranian Churn Dataset

**Date:** 2026-09-29  
**Decision Maker:** Sơn (Team Member 2)  
**Status:** ✅ Implemented  
**Impact:** 🔴 BREAKING CHANGE

### Context

The project initially used **Telco Customer Churn Dataset** (`WA_Fn-UseC_-Telco-Customer-Churn.csv`) from Kaggle with:
- 7,043 customers
- 21 columns (features like `customerID`, `gender`, `SeniorCitizen`, `Partner`, `MonthlyCharges`, `TotalCharges`, etc.)
- Target: `Churn` (Yes/No categorical)

However, the project requirements specified:
- **Iranian Churn Dataset** from UCI Machine Learning Repository
- 3,150 customers
- 13 features + 1 target
- Temporal structure: Use 9 months of data to predict 3-month churn

### Problem

The wrong dataset was being used:
- Telco dataset (Kaggle) ≠ Iranian dataset (UCI)
- Completely different schema (21 vs 14 columns)
- Different feature sets
- Different data source and structure
- All Week 1-2 work was based on wrong assumptions

### Decision

**Replace Telco Customer Churn dataset with Iranian Churn Dataset.**

### Rationale

1. **Project Requirements:** Project brief explicitly specifies Iranian Churn Dataset
2. **Team Agreement:** Project 15 scope is defined around Iranian dataset characteristics
3. **Correctness:** Using wrong dataset invalidates all modeling work
4. **Early Correction:** Better to fix in Week 2 than discover in Week 5

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| **Continue with Telco** | No rework needed | Wrong dataset, violates requirements | ❌ Rejected |
| **Use both datasets** | More data | Out of scope, confusing deliverables | ❌ Rejected |
| **Switch to Iranian** | Correct dataset, meets requirements | Requires rework of Week 1-2 | ✅ **Selected** |

### Implementation

#### Files Modified:
1. **Data Layer:**
   - `src/data.py` - Replaced Telco column schema with Iranian schema
   - `src/train.py` - Updated file path and references
   - `check_data.py` - Updated to load Iranian dataset

2. **Documentation:**
   - `data/README.md` - Full rewrite for Iranian dataset
   - `data/data_dictionary.csv` - Replaced 21 Telco columns with 14 Iranian columns
   - `docs/dataset-inspection.md` - Created comprehensive inspection report
   - `docs/decisions.md` - This file

3. **Code Changes:**
   - Removed Telco-specific logic (customerID, TotalCharges conversion, gender, etc.)
   - Removed `clean_telco_data()` function
   - Added Iranian-specific functions: `normalize_column_names()`, `validate_schema()`, `check_missing()`, `check_duplicates()`, `check_invalid_values()`, `basic_cleaning()`, `split_features_target()`
   - Updated `DEFAULT_EXPECTED_COLUMNS` to Iranian schema

#### Dataset Characteristics:

**Telco (OLD - WRONG):**
```
File: WA_Fn-UseC_-Telco-Customer-Churn.csv
Rows: ~7,043
Columns: 21
Features: customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges
Target: Churn (Yes/No string)
```

**Iranian (NEW - CORRECT):**
```
File: Customer Churn.csv
Rows: 3,150
Columns: 14 (13 features + 1 target)
Features: Call  Failure, Complains, Subscription  Length, Charge  Amount, Seconds of Use, Frequency of use, Frequency of SMS, Distinct Called Numbers, Age Group, Tariff Plan, Status, Age, Customer Value
Target: Churn (0/1 integer)
Churn Rate: 15.7%
Missing: None
Duplicates: None
MD5 Checksum: E5362C3E5787DADD4E21EB606509BC03
```

### Implications

#### ✅ Positive:
- Project now uses correct dataset per requirements
- Early correction minimizes wasted effort
- Proper foundation for Week 3+ work

#### ⚠️ Challenges:
- All Telco-based code invalidated
- Previous Week 2 baseline results discarded
- Need to re-run EDA, baseline models on Iranian dataset
- Column name whitespace issues (e.g., "Call  Failure" has 2 spaces)
- Feature definitions unknown (marked as "UNKNOWN - NEED VERIFICATION")
- Potential data leakage risks identified in `Status` and `Customer Value` columns

#### 🔴 Risks:
- **`Status` column:** May contain post-churn information (leakage risk)
- **`Customer Value` column:** 99.9% unique, may be ID or computed with leakage
- **Temporal structure:** Observation/prediction windows not explicit in CSV
- **Feature definitions:** Column meanings not documented, require UCI verification

### Follow-up Actions

#### Immediate (Week 2):
- [x] Replace dataset file in `data/raw/`
- [x] Update `src/data.py` with Iranian schema
- [x] Update `src/train.py` file path
- [x] Update `check_data.py`
- [x] Rewrite `data/README.md`
- [x] Rebuild `data/data_dictionary.csv`
- [x] Create `docs/dataset-inspection.md`
- [x] Document decision in `docs/decisions.md`
- [ ] Investigate `Status` column (leakage risk)
- [ ] Investigate `Customer Value` column (ID or feature?)
- [ ] Run EDA on train set (Iranian dataset)
- [ ] Train 3 baseline models (Iranian dataset)
- [ ] Update `docs/weekly/week-02.md` with correction story

#### Future (Week 3+):
- [ ] Find UCI documentation for feature definitions
- [ ] Verify observation/prediction window alignment
- [ ] Resolve leakage risks before advanced modeling
- [ ] Update `docs/project-brief.md` and `docs/baseline-plan.md` if needed

### Lessons Learned

1. **Verify dataset early:** Always confirm dataset source and schema before starting work
2. **Checksum verification:** Use MD5/SHA256 to verify dataset integrity
3. **Document assumptions:** Mark UNKNOWN items explicitly rather than guessing
4. **Early course correction:** Fixing wrong dataset in Week 2 is better than Week 5

### References

- Iranian Churn Dataset Inspection: `docs/dataset-inspection.md`
- Updated Data README: `data/README.md`
- Updated Data Dictionary: `data/data_dictionary.csv`
- Code changes: `src/data.py`, `src/train.py`, `check_data.py`

---

## Decision 002: Status and Customer Value - Keep Both Features

**Date:** 2026-09-29  
**Decision Maker:** Sơn (Team Member 2)  
**Status:** ✅ Implemented  
**Impact:** 🟢 LOW - Confirms features are valid

### Context

During Week 2 EDA, two features were flagged as potential risks:
1. **Status:** Potential data leakage (if reflects post-churn account status)
2. **Customer Value:** Potential ID column (due to high uniqueness)

Initial estimates suggested:
- Status distribution (76%/24%) was suspicious
- Customer Value was 99.94% unique (seemed like an ID)

Comprehensive analysis was required to determine if these features should be kept or dropped.

### Investigation Results

#### Status Column Analysis

**Distribution (Train Set):**
- Status=1: 1,301 samples (76.08%)
- Status=2: 409 samples (23.92%)

**Cross-tabulation with Churn:**
| Status | Churn=0 | Churn=1 | Churn Rate |
|--------|---------|---------|------------|
| 1 | 94.31% | 5.69% | **5.69%** |
| 2 | 52.57% | 47.43% | **47.43%** |

**Correlation:** 0.4898 (moderate, second strongest predictor)

**Leakage Assessment:**
- Max churn rate: 47.43% ✅ (below 80% threshold)
- Correlation: 0.4898 ✅ (below 0.7 threshold)
- Distribution mismatch with Churn: Status (76/24) ≠ Churn (84/16) ✅

**Interpretation:** Status likely represents:
- Contract type (e.g., monthly vs annual)
- Service tier (e.g., basic vs premium)
- Account category

It is NOT post-churn account status (which would show ~100% churn for cancelled accounts).

#### Customer Value Analysis

**Uniqueness (Train Set after duplicate removal):**
- Total rows: 1,710
- Unique values: 1,607
- Uniqueness: **93.98%** (NOT 99.94% as initially estimated)

**Descriptive Statistics:**
- Min: 0.00, Max: 2,165.28, Mean: 486.34, Median: 235.69
- Distribution: NOT sequential (many zeros), NOT uniform
- Clear business meaning: Higher values indicate more valuable customers

**Relationship with Churn:**
- Churn=0: Mean Customer Value = 552.45
- Churn=1: Mean Customer Value = 130.62
- **Churned customers have 76% lower Customer Value**

**Correlation:** -0.2921 (moderate negative, third strongest predictor)

**Assessment:**
- NOT an ID (93.98% unique, not 99%+)
- NOT sequential
- Valid business metric (likely CLV or account value)
- Strong predictive signal

### Decision

**✅ KEEP both Status and Customer Value as features**

### Rationale

#### Status:
1. **No Leakage Evidence:** Max churn rate (47.43%) well below 80% threshold
2. **Moderate Correlation:** 0.49 is strong signal but not suspicious (below 0.7)
3. **Genuine Predictive Power:** Status=2 has 8.3× higher churn rate than Status=1
4. **Valid Business Logic:** Likely represents contract/service differences
5. **Rank:** Second strongest predictor after Complains

#### Customer Value:
1. **Not an ID:** 93.98% unique (after duplicate removal) is reasonable for a value metric
2. **Business Meaning:** Clear interpretation as customer lifetime value or account value
3. **Predictive Signal:** Moderate correlation (-0.29), significant difference by churn
4. **Not Leakage:** No evidence of using post-churn information
5. **Rank:** Third strongest predictor (tied with Seconds of Use)

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| **Drop Status** | Conservative, eliminates any leakage risk | Loses second strongest predictor (0.49 corr) | ❌ Rejected |
| **Drop Customer Value** | Eliminates ID concern | Loses third strongest predictor (-0.29 corr) | ❌ Rejected |
| **Keep both with monitoring** | Uses all available signal | Requires model interpretation | ✅ **Selected** |
| **Drop both** | Ultra-conservative | Loses two top-5 predictors | ❌ Rejected |

### Implementation

#### Week 2 Baseline Models:
- ✅ Use all 13 features (including Status and Customer Value)
- ✅ StandardScaler for 10 numeric features (including Customer Value)
- ✅ Pass-through for 3 categorical features (including Status)

#### Monitoring Plan:
- ✅ Check Status coefficient in Logistic Regression
- ✅ Check Customer Value coefficient
- ✅ Compare model performance with/without these features (Week 3)
- ✅ Interpret SHAP values or feature importances (Week 3+)

### Implications

#### ✅ Positive:
- All 13 original features retained
- No information loss
- Maximum predictive power for baseline
- Clear decision backed by evidence

#### ⚠️ Risks Mitigated:
- Status: Confirmed not leakage via cross-tabulation
- Customer Value: Confirmed not ID via uniqueness and distribution analysis
- Both features have clear business interpretation

#### 📊 Expected Impact:
- Status: Likely to be highly important in models (correlation 0.49)
- Customer Value: Moderate importance (correlation -0.29)
- Combined with Complains (0.53), these top 3 features should drive most predictive power

### Follow-up Actions

#### Week 2 (Immediate):
- [x] Include Status and Customer Value in all 3 baseline models
- [x] Document decision in `docs/decisions.md`
- [x] Update `reports/data-quality-final.md`
- [x] Update `docs/weekly/week-02.md`

#### Week 3 (Future):
- [ ] Analyze Logistic Regression coefficients for Status and Customer Value
- [ ] Compare model performance with/without these features (ablation study)
- [ ] Interpret feature importances in advanced models
- [ ] Generate SHAP explanations if Status or Customer Value dominate

### Lessons Learned

1. **Don't guess from statistics alone:** Initial uniqueness estimate (99.94%) was based on raw data before duplicate removal
2. **Cross-tabulation is critical:** Status looked suspicious but cross-tab revealed safe usage
3. **Correlation thresholds work:** 0.49 correlation is strong but below 0.7 leakage threshold
4. **Business interpretation matters:** Customer Value uniqueness (93.98%) makes sense for a value metric
5. **Conservative approach has costs:** Dropping these features would lose significant predictive power

### References

- EDA Results: `reports/data-quality-final.md`
- EDA Script: `run_week2_eda.py`
- Visualizations: `reports/figures/status_vs_churn.png`, `customer_value_distribution.png`
- Correlation Matrix: `reports/figures/correlation_matrix.png`

---

## Decision Template (for future decisions)

```
## Decision XXX: [Title]

**Date:** YYYY-MM-DD
**Decision Maker:** Name
**Status:** Proposed / Approved / Implemented / Rejected
**Impact:** Low / Medium / High / Breaking

### Context
[Background and problem statement]

### Decision
[What was decided]

### Rationale
[Why this decision was made]

### Alternatives Considered
[Other options and why they were not chosen]

### Implementation
[How the decision was implemented]

### Implications
[Consequences, risks, and follow-up actions]

### References
[Related documents, code, or external resources]
```

---

**Document Status:** Active  
**Last Updated:** 2026-09-29  
**Next Review:** After Week 2 completion
