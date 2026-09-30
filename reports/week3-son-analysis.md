# Week 3 Analysis — Sơn

Phạm vi: chỉnh Week 3 để khớp đề giảng viên. Không làm Week 4, không đánh giá test, không chọn threshold cuối, không merge/cherry-pick, không commit/push và không sửa lịch sử Git.

## 1. Assignment alignment

Bài toán là binary classification bằng Logistic Regression, đầu ra là xác suất churn. Vòng thí nghiệm dùng split cố định, 5-fold StratifiedGroupKFold chỉ trên train, seed 42 và cùng folds cho sáu cấu hình C ∈ {0.1, 1, 10} × class_weight ∈ {None, balanced}. Toàn bộ imputer, scaler và encoder được fit trong fold-train. Candidate được chọn bằng mean train-CV PR_AUC; validation chỉ dùng để báo cáo candidate đã chọn. Test không được dự đoán.

B0 constant-probability baseline và B1 Logistic Regression baseline cũng được regenerate trên 13 features. B0 dùng train churn rate 0.157143; B1 dùng class_weight=None, C=1. Validation B1 đạt PR_AUC 0.747328, AP 0.748422, ROC_AUC 0.934781 và Brier 0.070479. Các baseline không thay đổi candidate selection rule.

## 2. Dataset provenance

- Dataset: Iranian Churn Dataset.
- Nguồn chính thức: UCI Machine Learning Repository, dataset ID 563.
- Trang nguồn: https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset
- DOI: https://doi.org/10.24432/C5JW3Z
- Citation: Iranian Churn [Dataset]. (2020). UCI Machine Learning Repository.
- Quy mô: 3.150 khách hàng, 13 features, không missing theo UCI.
- Raw file trong repo: data/raw/Customer Churn.csv.
- UCI hiện ghi license CC BY 4.0; ngày tải file vào repository không được ghi nhận.

UCI nêu mọi thuộc tính ngoài Churn được tổng hợp từ chín tháng đầu; Churn là trạng thái cuối tháng 12, tạo planning gap ba tháng.

## 3. Feature audit

| Feature | Type xử lý | Availability | Week 3 decision |
|---|---|---|---|
| Call Failure | numeric | first-nine-month aggregate | KEEP |
| Complains | categorical | first-nine-month aggregate | KEEP |
| Subscription Length | numeric | first-nine-month aggregate | KEEP |
| Charge Amount | numeric | first-nine-month aggregate | KEEP |
| Seconds of Use | numeric | first-nine-month aggregate | KEEP |
| Frequency of use | numeric | first-nine-month aggregate | KEEP |
| Frequency of SMS | numeric | first-nine-month aggregate | KEEP |
| Distinct Called Numbers | numeric | first-nine-month aggregate | KEEP |
| Age Group | categorical | first-nine-month aggregate | KEEP |
| Tariff Plan | categorical | first-nine-month aggregate | KEEP |
| Status | categorical | first-nine-month aggregate | KEEP |
| Age | numeric | first-nine-month aggregate | KEEP |
| Customer Value | numeric | first-nine-month aggregate | KEEP |
| Churn | target | outcome at month 12 | EXCLUDE FROM X |
| row_id | technical | loader identity | EXCLUDE FROM X |

Feature decisions dựa trên temporal metadata, không dựa trên correlation, uniqueness hay model performance.

## 4. Status decision

STATUS DECISION: KEEP.

UCI định nghĩa Status là 1=active, 2=non-active và đồng thời đặt mọi non-target attribute trong cửa sổ chín tháng đầu. Vì vậy biến có trước prediction point và không được mô tả là sử dụng nhãn churn tháng 12. Association cao với Churn không được dùng làm bằng chứng KEEP hoặc DROP.

## 5. Customer Value decision

CUSTOMER VALUE DECISION: KEEP.

UCI định nghĩa Customer Value là calculated value of customer và xác nhận mọi non-target attribute được tổng hợp trong chín tháng đầu. Điều này đủ để xác nhận temporal availability. Trang dataset công khai không nêu công thức chi tiết, nên công thức vẫn là caveat về diễn giải; không phải bằng chứng future leakage.

## 6. Final feature set

Feature set Week 3 là FINAL với 13 biến:

Call Failure, Complains, Subscription Length, Charge Amount, Seconds of Use, Frequency of use, Frequency of SMS, Distinct Called Numbers, Age Group, Tariff Plan, Status, Age, Customer Value.

So với run cũ, feature set đổi từ 11 lên 13 biến. Status và Customer Value đã được thêm vào src/features.py; toàn bộ CV, selection, validation và artifacts được regenerate. Churn và row_id vẫn bị loại khỏi X.

## 7. Preprocessing review

PREPROCESSING REVIEW = PASS.

- Numeric: median imputer rồi StandardScaler.
- Categorical: Complains, Age Group, Tariff Plan, Status; most-frequent imputer rồi OneHotEncoder(handle_unknown="ignore").
- Pipeline được fit mới trong từng fold-train.
- Fold-heldout và validation chỉ transform/predict, không refit.
- Unseen category được ignore, không học lại encoder.
- Test không tham gia fit, feature/model selection hoặc reporting.

## 8. class_weight analysis

So sánh cô lập tại C=1:

| class_weight | PR_AUC mean ± std | AP mean ± std | ROC_AUC mean | Brier mean | Precision mean | Recall mean | F1 mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| None | 0.742968 ± 0.067981 | 0.745753 ± 0.067056 | 0.929018 | 0.072627 | 0.806210 | 0.441186 | 0.560666 |
| balanced | 0.737933 ± 0.071805 | 0.740859 ± 0.070755 | 0.930645 | 0.111111 | 0.492276 | 0.885650 | 0.631505 |

Balanced tăng recall nhưng giảm precision và làm Brier xấu hơn. Không có lựa chọn tốt tuyệt đối về business cost; theo metric selection chính, unweighted tốt hơn tại C=1. Threshold 0.5 chỉ dùng để báo cáo, không phải threshold cuối.

## 9. C analysis

| class_weight | C | PR_AUC mean ± std | AP mean ± std | ROC_AUC mean | Brier mean |
|---|---:|---:|---:|---:|---:|
| None | 0.1 | 0.726344 ± 0.068166 | 0.729622 ± 0.066907 | 0.924767 | 0.075001 |
| None | 1 | 0.742968 ± 0.067981 | 0.745753 ± 0.067056 | 0.929018 | 0.072627 |
| None | 10 | 0.752463 ± 0.069578 | 0.755157 ± 0.068643 | 0.931712 | 0.071827 |
| balanced | 0.1 | 0.718777 ± 0.067492 | 0.722202 ± 0.066302 | 0.926279 | 0.114568 |
| balanced | 1 | 0.737933 ± 0.071805 | 0.740859 ± 0.070755 | 0.930645 | 0.111111 |
| balanced | 10 | 0.745701 ± 0.070387 | 0.748578 ± 0.069352 | 0.932734 | 0.109759 |

C=10 có mean PR_AUC cao nhất trong cả hai nhóm weight, nhưng chênh lệch giữa cấu hình nhỏ hơn fold variability; kết quả là selection theo rule đã khai báo, không phải khẳng định chắc chắn về superiority.

## 10. AP analysis

AP là Average Precision, tức weighted mean của precision theo các bước tăng recall. AP được giữ như metric phụ, tách biệt với PR_AUC. Candidate có train-CV AP 0.755157 ± 0.068643 và validation AP 0.761101.

## 11. PR_AUC analysis

PR_AUC là diện tích dưới precision-recall curve bằng trapezoidal integration trên recall tăng dần. Đây là metric selection chính theo đề. AP và PR_AUC cùng được tính nhưng không bị đồng nhất. Candidate có train-CV PR_AUC 0.752463 ± 0.069578 và validation PR_AUC 0.760070.

## 12. ROC_AUC

Candidate đạt train-CV ROC_AUC 0.931712 ± 0.020389 và validation ROC_AUC 0.936493. ROC_AUC là metric báo cáo, không dùng để đổi candidate sau selection.

## 13. Brier

Candidate đạt train-CV Brier 0.071827 ± 0.011535 và validation Brier 0.069941. Unweighted có Brier tốt hơn balanced trong grid này. Brier thấp hơn không thay thế calibration-curve review.

## 14. Candidate selection

OLD CANDIDATE: LogisticRegression, class_weight=None, C=10, được chọn trước đây bằng mean CV Average Precision trên feature set 11 biến.

NEW PR_AUC-BASED CANDIDATE: LogisticRegression, class_weight=None, C=10, được chọn bằng highest mean train-CV PR_AUC trên feature set 13 biến. Tie-break deterministic: giữ cấu hình xuất hiện trước trong declared order nếu cách best không quá 1e-6.

Candidate unchanged after aligning selection metric with assignment, nhưng model artifact và metrics đã thay đổi vì Status và Customer Value được thêm vào. Validation không được dùng để chọn lại candidate.

## 15. Validation metrics

| Metric | Value |
|---|---:|
| PR_AUC | 0.760070 |
| AP | 0.761101 |
| ROC_AUC | 0.936493 |
| Brier | 0.069941 |
| Precision | 0.807018 |
| Recall | 0.464646 |
| F1 | 0.589744 |
| Predicted positive | 57 |
| TN | 520 |
| FP | 11 |
| FN | 53 |
| TP | 46 |

Đây là validation 630 mẫu, không phải test.

## 16. Confusion matrix

Ở threshold tạm 0.5: TN=520, FP=11, FN=53, TP=46. Model cảnh báo khá thận trọng: precision khoảng 0.807 nhưng chỉ bắt được khoảng 46.5% churn. False negatives lớn hơn false positives; Week 3 không dùng quan sát này để tối ưu threshold.

## 17. Calibration

Validation Brier là 0.069941. Candidate calibration bins:

| Bin | Count | Mean probability | Observed churn rate |
|---:|---:|---:|---:|
| 0 | 412 | 0.0152 | 0.0170 |
| 1 | 47 | 0.1485 | 0.0851 |
| 2 | 32 | 0.2414 | 0.2188 |
| 3 | 38 | 0.3554 | 0.3158 |
| 4 | 44 | 0.4385 | 0.5227 |
| 5 | 10 | 0.5669 | 0.5000 |
| 6 | 4 | 0.6233 | 0.7500 |
| 7 | 0 | — | — |
| 8 | 6 | 0.8388 | 0.8333 |
| 9 | 37 | 0.9653 | 0.8919 |

Bin 0 có nhiều mẫu và khá sát ideal. Các bin 5, 6 và 8 nhỏ nên không overclaim. Bin cao nhất hơi overconfident. Không fit calibration model ở Week 3.

## 18. Tests

Unit test độc lập của Sơn kiểm tra:

- final 13-feature eligibility; target/technical không vào X;
- AP và true PR_AUC đều finite, nằm trong [0,1] và được trả về riêng;
- split/data invariants của Week 2.

Bốn integration tests kiểm tra no-refit preprocessing, bounded probabilities, grouped CV overlap và test_evaluated=false. Trên branch Son chúng conditional skip vì implementation runner của Thắng không được copy/merge.

- Branch Son: 14 total, 10 passed, 0 failed, 4 skipped.
- Isolated snapshot có implementation Thắng và feature set mới: 17 total, 17 passed, 0 failed, 0 skipped.

## 19. Remaining blockers

Không còn blocker làm thay đổi feature set hoặc candidate Week 3.

Caveat còn lại:

- Ngày tải raw file vào repo không được ghi nhận.
- Công thức chi tiết Customer Value chưa được công bố trên trang UCI, nên không diễn giải sâu cơ chế tạo biến.
- Runner/pipeline của Thắng chưa được tích hợp vào branch Son theo đúng yêu cầu không merge/cherry-pick; artifacts rerun được tạo từ isolated snapshot, không dùng test.

## 20. Week 4 handoff

Week 3 của Sơn đã đủ để handoff: 13-feature set đã chốt theo official temporal metadata; primary metric là PR_AUC; candidate và validation artifacts đã regenerate; test vẫn đóng. Nhóm cần tích hợp code theo workflow được phê duyệt và chạy lại full integration suite trên branch chung trước Week 4. Không có hoạt động Week 4 trong thay đổi này.

## Checksum note

- Exact CRLF checkout MD5: e5362c3e5787dadd4e21eb606509bc03.
- Exact CRLF checkout SHA256: 90d5fb6bd1630cd4de4b4d28fcf8b4cb92a8f6ab7484605b0799d47386f7dbe1.
- LF-normalized MD5: 07311e7080c0fb5b0ce94f5977abc4d5.
- LF-normalized SHA256: 72a4a660cba4166bab4f0c24e930d5453d1917e208c9ce2ed16b841347350dd3.

Khác biệt byte-level chỉ do line endings. Logical rows, row_id và frozen split 1.890/630/630 không đổi; không tạo split mới.
