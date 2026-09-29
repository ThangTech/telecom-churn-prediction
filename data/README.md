# Dữ liệu dự án: Dự đoán khách hàng rời mạng

## 1. Mục tiêu

Dự án này sử dụng **Iranian Churn Dataset** để dự đoán khả năng một khách hàng viễn thông sẽ rời mạng (churn) trong thời gian tới. Mô hình được xây dựng để hỗ trợ đội chăm sóc khách hàng, ưu tiên kiểm tra các khách hàng có nguy cơ cao và đưa ra các hành động tương ứng.

## 2. Nguồn dữ liệu

### Dataset Information
- **Dataset Name:** Iranian Churn Dataset
- **Source:** UCI Machine Learning Repository (verification pending)
- **Original Filename:** `Customer Churn.csv`
- **Local Path:** `data/raw/Customer Churn.csv`
- **MD5 Checksum:** `E5362C3E5787DADD4E21EB606509BC03`

### Dataset Specifications
- **Total Customers:** 3,150
- **Total Columns:** 14 (13 features + 1 target)
- **Target Variable:** `Churn` (binary: 0/1)
- **Class Distribution:**
  - No Churn (0): 2,655 customers (84.3%)
  - Churn (1): 495 customers (15.7%)
- **Missing Values:** None
- **Duplicate Rows:** None

### Temporal Structure
- **Observation Period:** UNKNOWN - NEED VERIFICATION (expected: 9 months)
- **Prediction Window:** UNKNOWN - NEED VERIFICATION (expected: 3 months)
- **Note:** Dataset does not contain explicit date/time columns. Features appear to be pre-aggregated over the observation period.

### Data Collection
- **Collection Method:** UNKNOWN - NEED VERIFICATION
- **Date Range:** UNKNOWN - NEED VERIFICATION
- **Geographic Region:** Iran (inferred from dataset name)

### License and Citation
- **License:** UNKNOWN - NEED VERIFICATION
- **Citation:** UNKNOWN - NEED VERIFICATION (UCI repository typically requires attribution)
- **Usage Terms:** Educational and research purposes (to be verified)

### Data Limitations
- Column definitions require verification from UCI documentation
- Temporal structure (observation/prediction windows) not explicitly documented in CSV
- Some column names contain extra whitespace (e.g., "Call  Failure")
- Potential data leakage risks identified in `Status` and `Customer Value` columns (see Section 8)

## 3. Cấu trúc dữ liệu

Mỗi dòng trong tập dữ liệu đại diện cho một khách hàng viễn thông duy nhất. Mỗi khách hàng có các thuộc tính:

- **Thông tin nhân khẩu học:** Age, Age Group
- **Hành vi sử dụng:** Call Failure, Seconds of Use, Frequency of use, Frequency of SMS, Distinct Called Numbers
- **Thông tin khiếu nại:** Complains
- **Thông tin tài chính:** Charge Amount, Customer Value
- **Thông tin hợp đồng:** Subscription Length, Tariff Plan, Status
- **Nhãn mục tiêu:** Churn (0 = No Churn, 1 = Churn)

## 4. Mục tiêu mô hình

- **Đầu vào:** Thông tin khách hàng và hành vi sử dụng trong observation period (9 months - to be verified)
- **Đầu ra:** Xác suất khách hàng rời mạng trong prediction window (3 months - to be verified)
- **Metric focus:** Recall (minimizing false negatives - miss churners is costly)
- **Vai trò:** Hỗ trợ ra quyết định của đội chăm sóc, không thay thế quyết định con người

## 5. Mô tả các tập dữ liệu

### data/raw/
Thư mục chứa dữ liệu gốc, chưa qua xử lý:

- **`Customer Churn.csv`** - Iranian Churn Dataset (3,150 customers × 14 columns)
- **Lưu ý:** 
  - Một số tên cột có whitespace thừa (e.g., "Call  Failure", "Subscription  Length", "Charge  Amount")
  - Code loader sẽ preserve tên gốc để trùng khớp với raw file
  - Không sửa file raw trực tiếp

### data/processed/
Thư mục chứa dữ liệu đã xử lý:

- `split_indices.json`: Chỉ số chia train/validation/test (nếu được tạo)
- Các file preprocessed features (fit trên train set only)
- Preprocessor artifacts (scalers, encoders) đã fit

### data/data_dictionary.csv
Bảng mô tả từng cột dữ liệu của Iranian Churn Dataset: tên cột, kiểu dữ liệu, mô tả (nếu có), role trong model, và các lưu ý về data quality.

## 6. Schema và Features

### 13 Features

#### Numeric Features (10):
1. **Call  Failure** (note: 2 spaces) - UNKNOWN - NEED VERIFICATION
2. **Complains** - UNKNOWN - NEED VERIFICATION  
3. **Subscription  Length** (note: 2 spaces) - UNKNOWN - NEED VERIFICATION (likely months)
4. **Charge  Amount** (note: 2 spaces) - UNKNOWN - NEED VERIFICATION
5. **Seconds of Use** - UNKNOWN - NEED VERIFICATION
6. **Frequency of use** - UNKNOWN - NEED VERIFICATION
7. **Frequency of SMS** - UNKNOWN - NEED VERIFICATION
8. **Distinct Called Numbers** - UNKNOWN - NEED VERIFICATION
9. **Age** - UNKNOWN - NEED VERIFICATION (actual age or derived?)
10. **Customer Value** - UNKNOWN - NEED VERIFICATION (⚠️ 99.9% unique - potential ID or leakage)

#### Categorical Features (3):
11. **Age Group** - Ordinal (1-5), UNKNOWN - NEED VERIFICATION
12. **Tariff Plan** - Nominal (1-2), UNKNOWN - NEED VERIFICATION
13. **Status** - Nominal (1-2), ⚠️ **POTENTIAL LEAKAGE RISK** - NEED VERIFICATION

### Target Variable
14. **Churn** - Binary (0 = No Churn, 1 = Churn)

## 7. Quy tắc dữ liệu và xử lý

### Data Security and Privacy
- Không lưu trữ thông tin cá nhân nhạy cảm nếu không cần thiết
- Dataset appears anonymized (no direct identifiers like phone numbers)
- If `Customer Value` is an ID, it should be dropped before training

### Feature Engineering Rules
- **Customer Value:** Check if ID or actual feature before using
- **Status:** Investigate correlation with Churn before using (leakage risk)
- **Age vs Age Group:** May be redundant, check correlation
- **Column name handling:** Preserve whitespace in column names to match raw CSV

### Preprocessing Requirements
- **NO preprocessing before train/validation/test split**
- Fit all transformers (scalers, encoders, imputers) on **train set only**
- Transform validation and test sets using fitted transformers
- Handle column name whitespace consistently

### Data Quality Checks
- ✅ No missing values (verified)
- ✅ No duplicate rows (verified)
- ⚠️ `Status` - potential leakage risk
- ⚠️ `Customer Value` - potential ID column (99.9% unique)

## 8. Biến nhãn (Target Variable)

- **Column Name:** `Churn`
- **Type:** Binary integer
- **Values:**
  - `0`: Customer did NOT churn (retained) - 2,655 cases (84.3%)
  - `1`: Customer DID churn (left) - 495 cases (15.7%)
- **Class Imbalance:** Moderate (15.7% positive class)
- **Handling:** Use stratified sampling for train/validation/test split
- **Modeling:** Consider `class_weight='balanced'` for Logistic Regression

## 9. Hướng dẫn sử dụng

### Tải dataset lại (nếu cần)
1. Download Iranian Churn Dataset from UCI ML Repository (URL pending verification)
2. Verify checksum: `E5362C3E5787DADD4E21EB606509BC03`
3. Place file as: `data/raw/Customer Churn.csv`
4. Do NOT modify raw file

### Workflow
1. **Load data:** Use `src/data.py::load_raw_data()`
2. **Validate schema:** Use `src/data.py::validate_schema()`
3. **Basic cleaning:** Use `src/data.py::basic_cleaning()` (deterministic only)
4. **Split data:** Use `src/data.py::build_train_validation_split()` (stratified)
5. **EDA:** Analyze train set only (see `src/train.py::run_eda()`)
6. **Preprocessing:** Fit transformers on train, transform val/test
7. **Modeling:** Train baseline models (Week 2), advanced models (Week 3+)
8. **Evaluation:** Use validation set for model selection, test set for final reporting

### Verification Commands
```bash
# Quick dataset check
python check_data.py

# Load and validate
python -c "from src.data import load_raw_data, validate_schema; df = load_raw_data('data/raw/Customer Churn.csv'); print(validate_schema(df))"

# Run full EDA
python src/train.py
```

## 10. Data Quality Issues and Risks

### Known Issues
1. **Column name whitespace:** Some columns have extra spaces (e.g., "Call  Failure")
   - **Resolution:** Code handles this by preserving original names
   
2. **`Status` column:** Potential data leakage risk
   - **Risk:** If Status reflects post-churn account status, it's target leakage
   - **Action:** Analyze Status vs Churn correlation before using as feature
   - **Status:** PENDING INVESTIGATION
   
3. **`Customer Value` column:** 99.9% unique values
   - **Risk:** Could be customer ID (should drop) or CLV with leakage
   - **Action:** Analyze distribution, relationship with Churn
   - **Status:** PENDING INVESTIGATION

4. **Temporal structure unclear:**
   - **Issue:** No explicit date columns, observation/prediction windows not documented
   - **Assumption:** Features pre-aggregated over 9-month observation period
   - **Status:** NEEDS VERIFICATION from UCI documentation

### Quality Assurance
- ✅ No missing values detected
- ✅ No duplicate rows detected
- ⚠️ Feature definitions require verification
- ⚠️ Leakage risks identified, require investigation

## 11. Lưu ý quan trọng

### Legal and Ethical
- Dataset appears to be from UCI ML Repository (public, educational use)
- Verify license and citation requirements before publication
- No obvious PII (personally identifiable information) in dataset
- Results should support human decision-making, not replace it

### Technical
- Column names with whitespace require careful handling in code
- Dataset is small (3,150 samples) - be cautious of overfitting
- Class imbalance (15.7% churn) requires stratified sampling
- Potential leakage risks require thorough investigation before Week 3

### Project Scope
- **Week 2:** Data quality, EDA, baseline models
- **Week 3+:** Feature engineering, advanced models, tuning
- Do NOT proceed to Week 3 until data quality issues are resolved

## 12. Changelog

### 2026-09-29: Dataset Correction (Sơn)
- **BREAKING CHANGE:** Replaced Telco Customer Churn with Iranian Churn Dataset
- **Reason:** Original dataset did not match project requirements
- **Impact:** All previous Telco-based code and results are invalidated
- **Updated files:** 
  - `data/README.md` (this file)
  - `data/data_dictionary.csv`
  - `src/data.py`
  - `src/train.py`
  - `check_data.py`
  - Documentation: `docs/dataset-inspection.md`, `docs/decisions.md`

### Future Updates
- Add UCI source URL once verified
- Add license and citation information
- Update feature definitions from UCI documentation
- Resolve `Status` and `Customer Value` investigation findings
