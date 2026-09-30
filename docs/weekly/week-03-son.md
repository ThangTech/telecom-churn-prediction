# Week 3 — Phan Duy Sơn

## Phạm vi

Chỉnh Week 3 để khớp đề giảng viên: Logistic Regression probability model, train-only 5-fold CV, thí nghiệm C/class_weight, true PR_AUC, AP riêng biệt, validation/calibration/confusion matrix, candidate artifact và preprocessing tests. Không làm Week 4, không đánh giá test, không chọn threshold cuối, không merge/cherry-pick, không commit/push.

## Assignment alignment

- Dataset: Iranian Churn Dataset, 3.150 khách hàng, 13 features.
- Nguồn: UCI Machine Learning Repository, dataset 563, DOI 10.24432/C5JW3Z.
- Prediction point: attributes trong chín tháng đầu; Churn ở cuối tháng 12.
- Fixed split: train/validation/test = 1.890/630/630, seed 42, duplicate-content grouped.
- CV: 5-fold StratifiedGroupKFold chỉ trên train, cùng folds cho mọi cấu hình.
- Primary selection metric: mean train-CV PR_AUC.
- Secondary metric: Average Precision.
- Test set: untouched.
- B0 constant train-rate và B1 Logistic Regression baseline đã regenerate trên 13 features; artifacts ghi test_evaluated=false.

## Feature decisions

UCI định nghĩa Status là 1=active, 2=non-active và Customer Value là calculated value of customer; UCI cũng xác nhận mọi non-target attribute được tổng hợp trong chín tháng đầu.

- Status: KEEP.
- Customer Value: KEEP.
- Exact Customer Value formula: chưa có trên public UCI page; giữ làm documentation caveat.
- Churn: target, loại khỏi X.
- row_id: technical, loại khỏi X.
- Final Week 3 feature set: 13 features.
- Feature set changed: YES, từ 11 lên 13; toàn bộ CV/selection/validation artifacts đã regenerate.

## Preprocessing review

PASS.

Numeric dùng median imputer + StandardScaler. Categorical gồm Complains, Age Group, Tariff Plan, Status, dùng most-frequent imputer + OneHotEncoder(handle_unknown="ignore"). Mỗi CV fold fit riêng trên fold-train; heldout/validation không refit; test không được sử dụng.

## Experiments và candidate

Grid: C ∈ {0.1, 1, 10}; class_weight ∈ {None, balanced}.

| Run | PR_AUC mean ± std | AP mean ± std | ROC_AUC mean | Brier mean |
|---|---:|---:|---:|---:|
| B1_C0.1 | 0.726344 ± 0.068166 | 0.729622 ± 0.066907 | 0.924767 | 0.075001 |
| B1_C1 | 0.742968 ± 0.067981 | 0.745753 ± 0.067056 | 0.929018 | 0.072627 |
| B1_C10 | 0.752463 ± 0.069578 | 0.755157 ± 0.068643 | 0.931712 | 0.071827 |
| M1_C0.1 | 0.718777 ± 0.067492 | 0.722202 ± 0.066302 | 0.926279 | 0.114568 |
| M1_C1 | 0.737933 ± 0.071805 | 0.740859 ± 0.070755 | 0.930645 | 0.111111 |
| M1_C10 | 0.745701 ± 0.070387 | 0.748578 ± 0.069352 | 0.932734 | 0.109759 |

Candidate cũ: class_weight=None, C=10, chọn bằng AP trên 11 features.

Candidate mới: class_weight=None, C=10, chọn bằng PR_AUC trên 13 features. Candidate configuration unchanged after aligning selection metric with assignment; metrics và serialized model đã đổi.

## Validation

- PR_AUC: 0.760070.
- AP: 0.761101.
- ROC_AUC: 0.936493.
- Brier: 0.069941.
- Precision: 0.807018.
- Recall: 0.464646.
- F1: 0.589744.
- TN=520, FP=11, FN=53, TP=46.
- Threshold 0.5 chỉ dùng báo cáo, không phải threshold cuối.

Calibration: bin lớn nhất (bin 0, n=412) có mean probability 0.0152 và observed rate 0.0170. Các bin 5/6/8 nhỏ nên không overclaim; bin cao nhất hơi overconfident. Không fit Platt/Isotonic.

## Artifacts

Created:

- src/metrics.py
- configs/experiments.json
- configs/baselines.json
- reports/week3_experiments.csv
- reports/week3_cv_folds.csv
- reports/week3_validation.csv
- reports/week3_calibration_bins.csv
- reports/validation_baselines.csv
- models/b1_pipeline.joblib
- models/week3_candidate.joblib
- reports/figures/son/validation_calibration.png
- reports/figures/son/validation_confusion_matrix.png

Updated:

- src/features.py
- tests/test_son_week3.py
- tests/test_week2.py
- data/README.md
- data/data_dictionary.csv
- docs/decisions.md
- reports/leakage-audit.md
- reports/data-quality.md
- reports/week3-son-analysis.md
- docs/weekly/week-03-son.md
- scripts/validate_week2.py

## Tests

Branch Son giữ bốn integration tests conditional-skip vì code runner/pipeline của Thắng chưa được merge/copy vào Son. Unit tests độc lập của Sơn gồm test true PR_AUC finite/bounded/distinct from AP.

- Branch Son: 14 total, 10 passed, 0 failed, 4 skipped.
- Isolated snapshot có implementation Thắng và feature set mới: 17 total, 17 passed, 0 failed, 0 skipped.

## Provenance/checksum

Official source: https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset

- CRLF SHA256: 90d5fb6bd1630cd4de4b4d28fcf8b4cb92a8f6ab7484605b0799d47386f7dbe1.
- LF-normalized MD5: 07311e7080c0fb5b0ce94f5977abc4d5.

Khác checksum do line endings; logical content, row_id và split không đổi. Ngày tải raw file vào repo không được ghi nhận.

## Remaining caveats và handoff

Không còn blocker làm thay đổi Week 3 feature set/candidate. Còn caveat về exact Customer Value formula, download date và group integration. Week 3 Sơn sẵn sàng handoff; trước Week 4, nhóm cần tích hợp theo workflow được phê duyệt và chạy lại integration suite trên branch chung.

## Commit/PR

Không tạo commit hoặc push theo yêu cầu.
