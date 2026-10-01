# Week 4 — Phan Duy Sơn (Correction Audit)

## Correction status

PASS. CV 13-feature đã được xác minh. UCI đặt Customer Value trong các non-target attributes của observation window chín tháng đầu nên quyết định KEEP; exact formula unknown được giữ như limitation, không coi là leakage. Threshold được chọn trên validation trước test, giữ nguyên sau train+validation refit; realized capacity được diễn giải là approximate. Test không rerun và không được dùng để tuning.

## Công việc thực hiện

- Rà soát 13-feature set theo UCI temporal metadata; approval status FINAL.
- Freeze Logistic Regression class_weight=None, C=10 từ train-only CV PR_AUC.
- Chọn ba probability thresholds từ validation theo capacity 10%/20%/30%.
- Chọn MEDIUM threshold 0.343183 làm operating point chính trước test.
- Tạo frozen evaluation config với checksum, split, preprocessing, model và thresholds.
- Chạy test đúng một final reporting event sau khi gate/preflight pass.
- Tạo confusion matrix, calibration, coefficient và error-analysis artifacts.
- Viết model card nháp và Week 4 tests.
- Không dùng test để tune; không làm API/Web hoặc Week 5.

## Frozen decisions

- Features: 13; Status KEEP, Customer Value KEEP.
- Feature-set status: FINAL.
- Model: LogisticRegression, class_weight=None, C=10, seed 42.
- Final fit: train+validation.
- Selection: mean train-CV PR_AUC.
- LOW threshold: 0.476833.
- MEDIUM threshold: 0.343183.
- HIGH threshold: 0.165057.
- Primary: MEDIUM, vì assumed care-team capacity khoảng 20%.

## Final test

Test evaluation count: 1.

- PR_AUC: 0.796582.
- AP: 0.798105.
- ROC_AUC: 0.949951.
- Brier: 0.062798.
- Precision: 0.678261.
- Recall: 0.787879.
- F1: 0.728972.
- TN=494, FP=37, FN=21, TP=78.

Test coverage tại LOW/MEDIUM/HIGH lần lượt là 11.27%, 18.25% và 26.98%. Threshold không được điều chỉnh theo test.

## Analysis summary

- Calibration nhìn chung tốt theo Brier nhưng có deviation ở một số mid-probability bins; bins 6–8 nhỏ.
- Low Subscription Length group có nhiều false positives và precision thấp hơn.
- Low Charge Amount group lớn, churn rate cao hơn và chứa nhiều absolute errors.
- Coefficients chỉ mô tả association với prediction; numeric coefficients là per-standard-deviation.
- B1 C=1 và final C=10 có ranking metrics gần nhau; final threshold tăng recall theo capacity objective.

## Main artifacts

- configs/week4_frozen_evaluation.json
- data/processed/split_indices.json
- reports/week4_thresholds_validation.csv
- reports/week4_test_final.csv
- reports/week4_test_thresholds.csv
- reports/week4_test_calibration_bins.csv
- reports/week4_coefficients.csv
- reports/week4_error_by_tenure.csv
- reports/week4_error_by_charge.csv
- reports/week4_baseline_comparison.csv
- reports/figures/son/week4_*.png
- models/week4_final_candidate.joblib
- docs/model-card-draft.md
- reports/week4-son-analysis.md
- tests/test_son_week4.py

## Protocol compliance

- Feature/model/threshold frozen before test: YES.
- Test used for tuning: NO.
- Test evaluation count: 1.
- Decisions changed after test: NO.
- Commit/push: NO.
- Test used for tuning: NO.
- Test contamination: NONE FOR THE REPORTED FROZEN EVALUATION.
- Capacity caveat: realized coverage sau refit là approximate; đây không phải test leakage.

## Tests

- Branch Sơn correction suite: 27 total, 23 passed, 0 failed, 4 conditional skips do runner/pipeline Thắng chưa được merge.

## Week 5 handoff

Week 4 correction hoàn tất và sẵn sàng Week 5. Exact Customer Value formula và realized-capacity drift sau refit được giữ trong limitations. Không được mở lại test hiện tại để tuning.
