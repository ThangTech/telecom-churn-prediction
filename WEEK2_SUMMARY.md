# 📊 WEEK 2 SUMMARY - SƠN

**Status:** ✅ **HOÀN TẤT 100%**  
**Date:** 2026-09-29

---

## ✅ ĐÃ HOÀN THÀNH (33/33 tasks)

### 🔧 Technical Setup
- ✅ Python 3.11.9 installed + venv configured
- ✅ All dependencies installed

### 📦 Dataset
- ✅ Iranian Churn Dataset verified
- ✅ **300 duplicates removed** (9.52%) → 2,850 unique rows
- ✅ 0 missing values
- ✅ Train/Val/Test: **60%/20%/20%** (1,710/570/570)
- ✅ Perfect stratification (84.33% / 15.67% in all sets)

### 🔍 EDA (Train Set: 1,710 rows)
- ✅ Descriptive statistics: All 13 features
- ✅ Correlation matrix computed
- ✅ Outlier detection (IQR method)
- ✅ Feature scale analysis
- ✅ 5 visualizations generated (200 DPI)

### 🎯 CRITICAL DECISIONS

#### Status Column
- **Distribution:** Status=1 (76%), Status=2 (24%)
- **Churn Rates:** Status=1 (5.69%), Status=2 (47.43%)
- **Correlation:** +0.4898 (second strongest predictor)
- **Max churn:** 47.43% < 80% threshold ✅
- **DECISION:** ✅ **KEEP** (safe to use, not leakage)

#### Customer Value
- **Uniqueness:** 93.98% (NOT 99.9% after dup removal)
- **Correlation:** -0.2921 (third strongest)
- **Churned customers:** 76% lower value
- **DECISION:** ✅ **KEEP** (valid feature, not ID)

### 📊 TOP CORRELATIONS WITH CHURN

| Rank | Feature | Correlation | Type |
|------|---------|-------------|------|
| 1 | **Complains** | +0.5337 | 🔴 Strongest |
| 2 | **Status** | +0.4898 | 🟠 Second |
| 3 | **Frequency of use** | -0.2952 | 🟡 Third |
| 4 | **Seconds of Use** | -0.2921 | 🟡 Third (tied) |
| 5 | **Customer Value** | -0.2921 | 🟡 Third (tied) |

---

## 📁 DELIVERABLES

### Code (3 files)
1. `run_week2_eda.py` - Comprehensive EDA script (400+ lines)
2. `src/data.py` - Split function fixed (60/20/20)
3. `run_eda.bat` - Venv activation wrapper

### Documentation (4 files)
1. `reports/data-quality-final.md` - Complete analysis (700+ lines)
2. `docs/decisions.md` - Decision 002 (Status & Customer Value)
3. `WEEK2_FINAL_CHECKPOINT.md` - Detailed checkpoint
4. `WEEK2_SUMMARY.md` - This file

### Visualizations (5 files)
1. `target_distribution.png`
2. `correlation_matrix.png`
3. `status_vs_churn.png`
4. `customer_value_distribution.png`
5. `feature_distributions.png`

---

## 🎯 FEATURES FOR BASELINE MODELS

### ✅ ALL 13 FEATURES VALIDATED (use ALL)

**Numeric (10):**
1. Call Failure
2. Complains ⭐ (strongest predictor)
3. Subscription Length
4. Charge Amount
5. Seconds of Use ⭐
6. Frequency of use ⭐
7. Frequency of SMS
8. Distinct Called Numbers
9. Age
10. **Customer Value** ⭐ (KEEP)

**Categorical (3):**
11. Age Group
12. Tariff Plan
13. **Status** ⭐ (KEEP - second strongest)

---

## 🔐 DATA QUALITY SCORE

### ⭐⭐⭐⭐⭐ (5/5 stars)

| Dimension | Score | Status |
|-----------|-------|--------|
| Completeness | 5/5 | 0 missing |
| Uniqueness | 5/5 | 300 dups removed |
| Validity | 5/5 | All values valid |
| Consistency | 5/5 | Types consistent |
| Leakage | 5/5 | No leakage detected |

---

## 📋 PREPROCESSING PLAN

### Configuration
```python
# StandardScaler for 10 numeric features
# Pass-through for 3 categorical (already numeric)
# Fit on train only → Transform val/test
```

### Decisions
- ✅ Use StandardScaler (required for LR)
- ✅ Fit on train only (prevent leakage)
- ✅ No outlier removal (keep all data)
- ✅ All 13 features included
- ✅ Stratified sampling (already done)

---

## 🚫 BLOCKERS

**Current:** ✅ **NONE** (all resolved)

Previously resolved:
1. ✅ Python environment → Installed
2. ✅ Split ratio wrong → Fixed to 60/20/20
3. ✅ Duplicates → Removed 300
4. ✅ Status concern → Investigated, KEEP
5. ✅ Customer Value concern → Investigated, KEEP

---

## 📊 BASELINE READINESS

### ✅ READY TO PROCEED

**Checklist:**
- [x] Dataset cleaned (2,850 rows)
- [x] Split verified (60/20/20, stratified)
- [x] All 13 features validated
- [x] Preprocessing plan finalized
- [x] No data leakage
- [x] Visualizations generated
- [x] Documentation complete

### Baseline Models (Week 3 - Not Week 2)
1. Churn-rate baseline (predict majority)
2. Logistic Regression (default)
3. Logistic Regression (class_weight='balanced')

---

## 📈 KEY INSIGHTS

### Data Characteristics
- **Size:** 2,850 customers (after removing 300 dups)
- **Churn rate:** 15.67% (moderate)
- **Class imbalance:** 5.38:1 (manageable)
- **Quality:** Perfect (no missing, no invalid)

### Predictive Signals
1. **Complaints matter most** (0.53 correlation)
2. **Status is critical** (0.49 correlation, 8.3× churn difference)
3. **Usage reduces churn** (negative correlations)
4. **Customer value matters** (-0.29 correlation)

### Safe to Use
- ✅ Status: NOT leakage (max churn 47%)
- ✅ Customer Value: NOT ID (93.98% unique, valid metric)
- ✅ All 13 features validated

---

## 🎯 WEEK 2 STATUS

| Metric | Status |
|--------|--------|
| **WEEK 2 COMPLETE** | ✅ YES (100%) |
| **EDA COMPLETE** | ✅ YES |
| **SPLIT VERIFIED** | ✅ YES (60/20/20) |
| **STATUS DECISION** | ✅ KEEP (safe) |
| **CUSTOMER VALUE DECISION** | ✅ KEEP (valid) |
| **BASELINE READY** | ✅ YES |
| **BLOCKERS** | ✅ NONE |

---

## 📁 FULL REPORTS

Detailed documentation in:
- `WEEK2_FINAL_CHECKPOINT.md` - Complete checkpoint (300+ lines)
- `reports/data-quality-final.md` - Full analysis (700+ lines)
- `docs/decisions.md` - Decision log (Decision 002)
- `reports/figures/` - 5 visualizations

---

## ✅ APPROVAL CHECKLIST

**Ready for your review:**
- [ ] Confirm Week 2 completion (100%) acceptable?
- [ ] Approve all 13 features for baseline?
- [ ] Approve Status decision (KEEP)?
- [ ] Approve Customer Value decision (KEEP)?
- [ ] Ready for Week 3? (Need separate instruction if yes)

---

**Status:** ✅ **WEEK 2 COMPLETE - AWAITING FINAL APPROVAL**

**Reporter:** Sơn (Team Member 2)  
**Project:** 15 - Telecom Customer Churn Prediction  
**Date:** 2026-09-29
