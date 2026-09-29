# Week 2 Progress Report

**Week:** 2  
**Date Range:** 2026-09-23 to 2026-09-29  
**Team Members:** Sơn (Data), Thắng (Baseline Models)  
**Project:** 15 - Telecom Customer Churn Prediction

---

## Overview

Week 2 focused on **dataset correction and data quality assessment**. A critical issue was discovered: the project was using the wrong dataset (Telco Customer Churn from Kaggle instead of Iranian Churn Dataset from UCI). This week involved correcting the dataset, updating all code and documentation, and preparing for baseline modeling.

---

## Major Accomplishments

### 1. Dataset Correction (Sơn) ✅

**Problem Discovered:**
- Project was using Telco Customer Churn dataset (7,043 customers, 21 columns)
- Should be using Iranian Churn Dataset (3,150 customers, 14 columns)
- Completely different schemas and data sources

**Resolution:**
- Located and verified Iranian Churn Dataset
- Replaced dataset in `data/raw/Customer Churn.csv`
- Updated all code references
- Updated all documentation

**Impact:**
- 🔴 BREAKING CHANGE - All previous Telco-based work invalidated
- ✅ Project now uses correct dataset per requirements
- ✅ Foundation established for Week 3+ work

**Details:** See `docs/decisions.md` - Decision 001

### 2. Dataset Inspection (Sơn) ✅

**Comprehensive inspection completed:**
- File verification: MD5 checksum `E5362C3E5787DADD4E21EB606509BC03`
- Shape: 3,150 rows × 14 columns (13 features + 1 target)
- Target: Churn (binary 0/1), 15.7% churn rate
- Quality: 100% complete (no missing values, no duplicates)
- Schema validation: All 14 expected columns present

**Findings:**
- ✅ Dataset quality is excellent
- ⚠️ Column name whitespace issues (e.g., "Call  Failure" has 2 spaces)
- ⚠️ `Status` column - potential data leakage risk (requires investigation)
- ⚠️ `Customer Value` - 99.9% unique, may be ID (requires investigation)
- ⚠️ Feature definitions unknown (require UCI documentation)

**Deliverables:**
- `docs/dataset-inspection.md` - Full inspection report (47 sections)
- `reports/data-quality.md` - Data quality assessment

### 3. Code Updates (Sơn) ✅

**Files Modified:**

#### src/data.py
- ✅ Replaced `DEFAULT_EXPECTED_COLUMNS` with Iranian dataset schema (14 columns)
- ✅ Removed `clean_telco_data()` function (Telco-specific)
- ✅ Added new functions:
  - `normalize_column_names()` - Handle column whitespace
  - `validate_schema()` - Schema validation against expected columns
  - `check_missing()` - Missing value detection
  - `check_duplicates()` - Duplicate row detection
  - `check_invalid_values()` - Data validation rules
  - `basic_cleaning()` - Deterministic cleaning only (no imputation/scaling)
  - `split_features_target()` - Separate X and y
- ✅ Documented column name mapping (whitespace handling)

#### src/train.py
- ✅ Updated `raw_path` to `"data/raw/Customer Churn.csv"`
- ✅ Replaced `clean_telco_data()` with `basic_cleaning()`
- ✅ Updated imports for new functions
- ✅ Fixed EDA plotting (removed customerID references)
- ✅ Updated categorical detection (Iranian dataset uses int64 for categories)

#### check_data.py
- ✅ Rewritten for Iranian dataset
- ✅ Now checks: shape, columns, target, missing, duplicates
- ✅ Added detailed output formatting

### 4. Documentation Updates (Sơn) ✅

#### data/README.md
- ✅ Complete rewrite for Iranian Churn Dataset
- ✅ Added dataset specifications (source, checksum, size, structure)
- ✅ Documented 13 features + 1 target
- ✅ Added data quality notes (missing=0, duplicates=0)
- ✅ Documented column name whitespace issues
- ✅ Added leakage risk warnings (Status, Customer Value)
- ✅ Included usage guidelines and workflow
- ✅ Added changelog entry for dataset correction

#### data/data_dictionary.csv
- ✅ Replaced 21 Telco columns with 14 Iranian columns
- ✅ Schema: column_name, data_type, description, unit, role, available_at, valid_values_or_rules, missing_policy, notes
- ✅ Marked unknown definitions as "UNKNOWN - NEED VERIFICATION"
- ✅ Documented leakage risks for Status and Customer Value
- ✅ Added distribution notes for categorical variables

#### docs/dataset-inspection.md
- ✅ Created comprehensive 47-section inspection report
- ✅ File information and checksum
- ✅ Shape validation (3,150 × 14)
- ✅ Complete schema with 14 columns
- ✅ Data quality assessment (missing, duplicates, invalid values)
- ✅ Target variable analysis (15.7% churn rate)
- ✅ Feature analysis (numeric and categorical)
- ✅ Leakage risk assessment
- ✅ Comparison with Telco dataset (old vs new)
- ✅ Recommendations and next steps

#### docs/decisions.md
- ✅ Created decisions log
- ✅ Documented Decision 001: Dataset Correction
- ✅ Included context, rationale, alternatives, implementation, implications
- ✅ Documented all modified files
- ✅ Comparison table: Telco (WRONG) vs Iranian (CORRECT)
- ✅ Listed follow-up actions and lessons learned

#### reports/data-quality.md
- ✅ Created comprehensive data quality report
- ✅ Quality score: 4/5 stars
- ✅ Schema validation results
- ✅ Missing values: 0 (100% complete)
- ✅ Duplicates: 0
- ✅ Target distribution analysis
- ✅ Feature analysis (numeric and categorical)
- ✅ Leakage risk assessment (Status and Customer Value)
- ✅ Preprocessing recommendations
- ✅ Unresolved issues (Critical: Status and Customer Value investigations)
- ✅ Next steps for Week 2 and Week 3

---

## Work Distribution

### Sơn's Scope (Data Layer) ✅
- [x] Dataset correction (locate, verify, replace)
- [x] Dataset inspection (comprehensive analysis)
- [x] Data quality assessment
- [x] Code updates (src/data.py, src/train.py, check_data.py)
- [x] Documentation updates (README, data_dictionary, inspection report, decisions log, quality report)
- [x] Schema validation
- [x] Leakage risk identification
- [ ] EDA on train set (BLOCKED - requires running Python environment)
- [ ] Status column investigation (BLOCKED - requires EDA)
- [ ] Customer Value investigation (BLOCKED - requires EDA)

### Thắng's Scope (Baseline Models)
- Split functionality exists in `src/data.py::build_train_validation_split()`
- Function signature: `(df, target_col="Churn", test_size=0.2, val_size=0.25, random_state=42)`
- Uses stratified sampling
- Status: CODE EXISTS but not verified with Iranian dataset
- Baseline models: NOT STARTED (depends on dataset correction completion)

---

## Technical Challenges

### 1. Python Environment Issue ⚠️
**Problem:** Python command not working in terminal (`Python không tìm thấy`)
**Impact:** Cannot run Python scripts for EDA, detailed statistics, or baseline models
**Workaround:** Used PowerShell `Import-Csv` for basic dataset verification
**Status:** UNRESOLVED - blocks EDA completion

### 2. Column Name Whitespace ⚠️
**Problem:** Three columns have extra internal spaces:
- `"Call  Failure"` (2 spaces)
- `"Subscription  Length"` (2 spaces)
- `"Charge  Amount"` (2 spaces)

**Solution:** Code preserves original names to match raw CSV
**Implementation:** `normalize_column_names()` only strips leading/trailing whitespace
**Status:** RESOLVED

### 3. Feature Definitions Unknown ⚠️
**Problem:** Column meanings not documented in CSV file
**Impact:** Cannot interpret model coefficients or validate domain rules
**Approach:** Marked all definitions as "UNKNOWN - NEED VERIFICATION"
**Status:** PENDING UCI documentation search

### 4. Data Leakage Risks ⚠️
**Problem:** Two columns flagged as potential leakage:
- `Status` (2 values: 1=75.2%, 2=24.8%) - unknown if post-churn status
- `Customer Value` (99.9% unique) - unknown if ID or CLV with leakage

**Required Action:** EDA investigation on train set only
**Status:** PENDING (blocked by Python environment)

---

## Deliverables

### Code Files ✅
- [x] `src/data.py` - Updated for Iranian dataset (added 7 new functions)
- [x] `src/train.py` - Updated file path and cleaning logic
- [x] `check_data.py` - Rewritten for Iranian dataset verification

### Documentation Files ✅
- [x] `data/README.md` - Complete rewrite (230 lines)
- [x] `data/data_dictionary.csv` - 14 Iranian columns with full schema
- [x] `docs/dataset-inspection.md` - Comprehensive inspection (450+ lines)
- [x] `docs/decisions.md` - Decisions log with Decision 001
- [x] `docs/weekly/week-02.md` - This file
- [x] `reports/data-quality.md` - Data quality assessment (550+ lines)

### Data Files ✅
- [x] `data/raw/Customer Churn.csv` - Iranian Churn Dataset (verified, MD5 checksum)

---

## Critical Findings

### ✅ Strengths
1. **Dataset Quality Excellent:** 100% complete, no missing values, no duplicates
2. **Target Variable Well-Defined:** Binary 0/1, 15.7% churn rate (realistic)
3. **Class Imbalance Manageable:** 5.36:1 ratio, sufficient minority samples (495)
4. **Code Foundation Solid:** Clean architecture, proper split logic exists
5. **Documentation Comprehensive:** All files updated with detailed information

### ⚠️ Concerns
1. **Status Column:** Potential leakage risk - MUST investigate before Week 3
2. **Customer Value:** 99.9% unique, may be ID - MUST investigate before Week 3
3. **Feature Definitions:** Unknown meanings - requires UCI documentation
4. **Temporal Structure:** Observation/prediction windows not explicit
5. **Python Environment:** Blocking EDA and model training

### 🔴 Blockers
1. **Python Environment Issue:** Cannot run scripts for EDA or modeling
2. **EDA Incomplete:** Status and Customer Value investigations pending
3. **Baseline Models:** Not started (depends on EDA completion and Python fix)

---

## Metrics and Statistics

### Dataset Metrics
| Metric | Value |
|--------|-------|
| Total Customers | 3,150 |
| Total Features | 13 |
| Target Variable | Churn (0/1) |
| Churn Rate | 15.7% (495/3,150) |
| No Churn | 84.3% (2,655/3,150) |
| Missing Values | 0 (100% complete) |
| Duplicate Rows | 0 |
| File Size | 0.20 MB |
| MD5 Checksum | E5362C3E5787DADD4E21EB606509BC03 |

### Feature Breakdown
| Type | Count | Examples |
|------|-------|----------|
| Numeric (int64) | 11 | Call Failure, Complains, Age, Churn |
| Numeric (float64) | 2 | Charge Amount, Customer Value |
| Categorical (low cardinality) | 3 | Age Group (5), Tariff Plan (2), Status (2) |
| Binary Target | 1 | Churn |

### Code Changes
| File | Lines Changed | Type |
|------|---------------|------|
| src/data.py | ~150 added, ~80 removed | Major refactor |
| src/train.py | ~20 changed | Updates |
| check_data.py | Full rewrite | Replacement |
| data/README.md | Full rewrite (230 lines) | Replacement |
| data/data_dictionary.csv | Full rewrite | Replacement |
| docs/dataset-inspection.md | 450+ lines | New |
| docs/decisions.md | 200+ lines | New |
| reports/data-quality.md | 550+ lines | New |

---

## Week 2 Completion Status

### Sơn's Tasks

#### ✅ Completed (9/12)
1. ✅ Dataset correction (locate, download, verify Iranian dataset)
2. ✅ Dataset inspection (comprehensive analysis with checksum)
3. ✅ Data quality assessment
4. ✅ Update src/data.py (remove Telco, add Iranian functions)
5. ✅ Update src/train.py (file path, imports, logic)
6. ✅ Update check_data.py (rewrite for Iranian)
7. ✅ Update data/README.md (full rewrite)
8. ✅ Update data/data_dictionary.csv (14 Iranian columns)
9. ✅ Create docs/dataset-inspection.md, docs/decisions.md, reports/data-quality.md

#### ⚠️ Blocked (3/12)
10. ⚠️ Run EDA on train set (BLOCKED by Python environment)
11. ⚠️ Investigate Status column (BLOCKED by Python environment)
12. ⚠️ Investigate Customer Value column (BLOCKED by Python environment)

**Completion Rate:** 75% (9/12 tasks)

### Thắng's Tasks

#### Status Unknown
- Split functionality code exists but not tested with Iranian dataset
- Baseline models not started
- Depends on Sơn's data layer completion

---

## Risks and Mitigation

| Risk | Impact | Probability | Mitigation | Status |
|------|--------|-------------|------------|--------|
| **Status leakage** | 🔴 HIGH | 🟡 MEDIUM | Investigate on train set; drop if leakage confirmed | ⚠️ PENDING |
| **Customer Value is ID** | 🔴 HIGH | 🟡 MEDIUM | Analyze distribution; drop if ID confirmed | ⚠️ PENDING |
| **Python environment** | 🟠 MEDIUM | 🔴 HIGH | Fix environment or use alternative tools | ⚠️ ACTIVE |
| **Feature definitions unknown** | 🟡 LOW | 🟢 LOW | Search UCI docs; proceed with "UNKNOWN" labels | ⚠️ ONGOING |
| **Temporal structure unclear** | 🟡 LOW | 🟢 LOW | Document assumption; treat as standard classification | ✅ DOCUMENTED |

---

## Lessons Learned

### What Went Well ✅
1. **Early Detection:** Dataset error caught in Week 2, not Week 5
2. **Systematic Approach:** Comprehensive inspection before coding
3. **Documentation First:** Updated docs alongside code
4. **Risk Identification:** Flagged leakage risks before modeling
5. **Code Quality:** Clean refactor, no Telco references remaining

### What Could Be Improved ⚠️
1. **Environment Setup:** Should verify Python environment earlier
2. **Dataset Verification:** Should check dataset source in Week 1
3. **Feature Documentation:** Should search UCI docs immediately after dataset identified
4. **Team Coordination:** Should coordinate with Thắng on split testing

### Action Items for Week 3
1. Fix Python environment (CRITICAL)
2. Complete EDA on train set
3. Resolve Status and Customer Value investigations
4. Test train/val/test split with Iranian dataset
5. Run baseline models (after investigations complete)
6. Search UCI repository for feature definitions
7. Update project-brief.md and baseline-plan.md if needed

---

## Next Week (Week 3) Preview

### Planned Activities (If Blockers Resolved)
1. Complete EDA on train set
2. Resolve Status and Customer Value investigations
3. Implement preprocessing pipeline (fit on train only)
4. Feature engineering (if needed, minimal for baseline)
5. Train 3 baseline models:
   - Churn-rate baseline (majority class)
   - Logistic Regression (default)
   - Logistic Regression (class_weight='balanced')
6. Evaluate models on validation set
7. Generate metrics: Precision, Recall, F1, PR-AUC, ROC-AUC
8. Threshold analysis for business decision making
9. Update weekly report

### Prerequisities
- ✅ Dataset corrected (Iranian Churn Dataset)
- ✅ Code updated (src/data.py, src/train.py)
- ✅ Documentation complete
- ⚠️ Python environment fixed
- ⚠️ EDA completed
- ⚠️ Leakage risks resolved

---

## Summary

Week 2 was a **critical correction week**. The major achievement was discovering and fixing the wrong dataset issue, which would have invalidated all future work. Despite Python environment challenges blocking EDA completion, significant progress was made:

- ✅ Dataset correction completed
- ✅ Code refactored for Iranian dataset
- ✅ Comprehensive documentation created
- ✅ Data quality assessed (excellent quality: no missing, no duplicates)
- ⚠️ Critical investigations identified (Status and Customer Value)
- ⚠️ EDA blocked by Python environment issue

**Week 2 Status:** ✅ **PARTIAL COMPLETION** (75% of Sơn's tasks done)

**Readiness for Week 3:** ⚠️ **CONDITIONAL** (requires Python environment fix and leakage investigations)

**Recommendation:** Fix Python environment, complete EDA and investigations, then proceed to baseline modeling.

---

**Report Author:** Sơn (Team Member 2)  
**Report Date:** 2026-09-29  
**Next Update:** Week 3 completion