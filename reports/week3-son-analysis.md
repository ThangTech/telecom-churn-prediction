# Week 3 Analysis — Sơn

Phạm vi review: snapshot mới nhất `origin/Thang` tại `7e3be82d`, gồm implementation ở `2d26f433` và `402f4fb5`. Branch hiện tại `Son` chưa tích hợp các commit này, vì vậy review được thực hiện read-only bằng `git show` và một snapshot tạm; không checkout, merge, commit, push hoặc đánh giá test set.

## 1. Mục tiêu

Hoàn thiện phần Week 3 cá nhân của Sơn: audit feature set, review preprocessing và kết quả validation/CV của Thắng, kiểm tra leakage theo prediction point, bổ sung tests thuộc phạm vi Sơn và ghi rõ các blocker còn mở. Feature set/model candidate không được gọi là final và test set tiếp tục được giữ đóng.

## 2. Feature audit

Prediction point theo đề: dùng thông tin chín tháng đầu để dự đoán churn trong ba tháng sau.

| Feature | data_type | role | available_at | Current status | Reason |
|---|---|---|---|---|---|
| Call  Failure | integer | feature | observation_window | USED | Có trong whitelist 11 feature; metadata chính thức vẫn cần bổ sung |
| Complains | integer/binary observed | feature | observation_window | USED | Được xử lý categorical; không giả định khoảng cách số |
| Subscription  Length | integer | feature | observation_window | USED | Có trong whitelist; định nghĩa/unit chính thức còn caveat |
| Charge  Amount | integer | feature | observation_window | USED | Có trong whitelist; aggregation definition còn caveat |
| Seconds of Use | integer | feature | observation_window | USED | Có trong whitelist |
| Frequency of use | integer | feature | observation_window | USED | Có trong whitelist |
| Frequency of SMS | integer | feature | observation_window | USED | Có trong whitelist |
| Distinct Called Numbers | integer | feature | observation_window | USED | Có trong whitelist |
| Age Group | integer/category | feature | static | USED | One-hot để không ép quan hệ tuyến tính/đều khoảng |
| Tariff Plan | integer/category | feature | static | USED | Mã danh mục, được one-hot |
| Age | integer | feature | static | USED | Có trong whitelist; reference date còn caveat |
| Status | integer/category | feature | UNKNOWN | PENDING | Không có định nghĩa hoặc thời điểm cập nhật đáng tin cậy |
| Customer Value | float | feature | UNKNOWN | PENDING | Không có công thức, input window hoặc calculation time |
| Churn | integer | target | outcome_window | EXCLUDED | Target, không được có trong X |
| row_id | integer | technical | load time | EXCLUDED | Chỉ dùng kiểm chứng split |

`CONFIRMED_MODEL_FEATURES` có 11 biến. `PENDING_VERIFICATION_FEATURES` gồm `Status` và `Customer Value`. Cấu hình thí nghiệm và `model_inputs()` khớp với danh sách này.

## 3. Status decision

**STATUS DECISION: UNRESOLVED — SOURCE VERIFICATION REQUIRED**

Repository không có định nghĩa chính thức, không xác nhận `Status` thuộc observation window và không chứng minh biến không dùng trạng thái hậu churn.

Thống kê train chỉ mang tính mô tả:

- Status 1: 1.427 mẫu; Status 2: 463 mẫu.
- Cross-tab: Status 1 có 1.347 non-churn và 80 churn; Status 2 có 246 non-churn và 217 churn.
- Churn rate: 5,61% ở Status 1 và 46,87% ở Status 2.
- Pearson association với Churn: khoảng 0,488.

Association mạnh không xác định thời điểm feature có sẵn. `Status` tiếp tục bị loại khỏi model.

## 4. Customer Value decision

**CUSTOMER VALUE DECISION: UNRESOLVED — SOURCE VERIFICATION REQUIRED**

Không có công thức hoặc bằng chứng rằng biến chỉ dùng dữ liệu chín tháng đầu. Không thể xác nhận đây là derived metric hợp lệ hay loại trừ future/outcome information.

Thống kê train chỉ mang tính mô tả:

- 1.623 giá trị unique trên 1.890 dòng, unique ratio 85,87%.
- Mean 470,67; median 228,48; min 0; max 2.148,03.
- Mean ở non-churn 534,59 và churn 127,80.
- Correlation với Churn khoảng -0,289.
- Association tuyệt đối lớn nhất với `Frequency of SMS` khoảng 0,920.

Uniqueness, distribution và correlation không chứng minh identifier/non-identifier hoặc temporal safety. Biến tiếp tục bị loại khỏi model.

## 5. Provisional feature set

Week 3 giữ nguyên 11 biến trong `CONFIRMED_MODEL_FEATURES`. `Status` và `Customer Value` tiếp tục nằm trong `PENDING_VERIFICATION_FEATURES`; `Churn` là target và `row_id` là technical identity. Đây là **provisional Week 3 feature set**, không phải feature set final. Nếu nhóm sau này xác nhận KEEP một pending feature, toàn bộ CV và candidate selection Week 3 phải được chạy lại trước khi chấp nhận candidate.

## 6. Preprocessing review

- Numeric: Call Failure, Subscription Length, Charge Amount, Seconds of Use, Frequency of use, Frequency of SMS, Distinct Called Numbers, Age.
- Categorical: Complains, Age Group, Tariff Plan.
- `Complains` là indicator 0/1 trong dữ liệu; xử lý categorical là hợp lý và tránh giả định khoảng cách liên tục.
- `Age Group` one-hot là lựa chọn thận trọng khi mapping/ordinal spacing chưa được xác minh.
- `Tariff Plan` phải được coi là nominal; one-hot phù hợp.
- Dataset hiện không missing nên imputer không thay đổi train data. Giữ imputer trong pipeline vẫn hợp lý cho robustness và không gây leakage vì nó fit trong fold-train.
- Median imputer + StandardScaler cho numeric và most-frequent imputer + OneHotEncoder cho categorical đều nằm trong `Pipeline`/`ColumnTransformer` và được fit lại ở mỗi CV fold.
- `handle_unknown="ignore"` xử lý unseen category mà không refit.
- Validation chỉ được transform/predict; test được unpack thành `_` và không được dự đoán trong scripts Week 3.

Không đề xuất đổi preprocessing ở vòng này.

## 7. class_weight analysis

So sánh cô lập tại C=1:

| class_weight | AP mean ± std | ROC-AUC mean ± std | Brier mean ± std | Precision mean ± std | Recall mean ± std | F1 mean ± std |
|---|---:|---:|---:|---:|---:|---:|
| None | 0,7357 ± 0,0710 | 0,9208 ± 0,0237 | 0,0740 ± 0,0109 | 0,8742 ± 0,1165 | 0,4178 ± 0,1206 | 0,5544 ± 0,1083 |
| balanced | 0,7274 ± 0,0746 | 0,9207 ± 0,0238 | 0,1195 ± 0,0169 | 0,4482 ± 0,0312 | 0,8892 ± 0,0709 | 0,5943 ± 0,0275 |

Unweighted ưu tiên precision và có Brier thấp hơn, nhưng bỏ sót nhiều churn hơn. Balanced tăng recall mạnh, đổi lại precision giảm, false-positive workload tăng và xác suất kém calibration hơn. Không có lựa chọn tốt hơn tuyệt đối: đội chăm sóc hạn chế phù hợp hơn với precision cao; mục tiêu giảm bỏ sót phù hợp hơn với recall cao. Threshold 0,5 chỉ là tạm thời và không được tối ưu ở Week 3.

## 8. C analysis

C nhỏ tương ứng regularization mạnh hơn; C lớn tương ứng regularization yếu hơn.

| class_weight | C | AP mean ± std | ROC-AUC mean | Brier mean | Precision mean | Recall mean | F1 mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| None | 0,1 | 0,7261 ± 0,0765 | 0,9162 | 0,0765 | 0,8990 | 0,4008 | 0,5465 |
| None | 1 | 0,7357 ± 0,0710 | 0,9208 | 0,0740 | 0,8742 | 0,4178 | 0,5544 |
| None | 10 | 0,7390 ± 0,0657 | 0,9226 | 0,0739 | 0,8501 | 0,4178 | 0,5508 |
| balanced | 0,1 | 0,7214 ± 0,0787 | 0,9174 | 0,1235 | 0,4441 | 0,8858 | 0,5903 |
| balanced | 1 | 0,7274 ± 0,0746 | 0,9207 | 0,1195 | 0,4482 | 0,8892 | 0,5943 |
| balanced | 10 | 0,7306 ± 0,0719 | 0,9216 | 0,1195 | 0,4481 | 0,8858 | 0,5936 |

C=10 unweighted được **selected by mean CV AP**. Chênh lệch AP giữa C=10 và C=1 chỉ khoảng 0,0033, nhỏ hơn nhiều so với fold standard deviation khoảng 0,066–0,071. Vì vậy không có bằng chứng rằng C=10 chắc chắn vượt trội; đây chỉ là ứng viên theo quy tắc selection đã công bố.

## 9. Candidate review

- Model: LogisticRegression.
- class_weight: None.
- C: 10.
- Selection: mean AP cao nhất trong CV train; không chọn lại bằng validation.
- Threshold 0,5: tạm thời.
- Status: provisional vì metadata của dataset và hai pending features chưa được xác minh.
- Model được fit trên train, không fit train+validation và không đánh giá test.

## 10. Validation metrics

| Metric | Value |
|---|---:|
| AP | 0,763925 |
| ROC-AUC | 0,933449 |
| Brier | 0,070677 |
| Precision | 0,884615 |
| Recall | 0,464646 |
| F1 | 0,609272 |
| Predicted positive | 52 |
| TN | 525 |
| FP | 6 |
| FN | 53 |
| TP | 46 |

Candidate xếp hạng tốt trên validation và tại threshold tạm 0,5 thiên về precision hơn recall. FP là sáu khách không churn nhưng bị cảnh báo, làm tăng workload chăm sóc. FN là 53 khách churn nhưng không được cảnh báo, thể hiện chi phí bỏ sót đáng kể. Không thay threshold trong Week 3.

## 11. Confusion matrix interpretation

Ma trận validation xác nhận TN=525, FP=6, FN=53, TP=46. Số false negative cao hơn false positive phù hợp với precision 0,885 và recall 0,465: model phát cảnh báo khá thận trọng. Đây không phải confusion matrix test.

## 12. Calibration interpretation

Candidate có Brier 0,0707, gần B1 C=1 và tốt hơn balanced C=1 (0,1121) trên validation. Các bin candidate:

| Bin | Count | Mean probability | Observed churn rate |
|---:|---:|---:|---:|
| 0 | 414 | 0,0166 | 0,0145 |
| 1 | 37 | 0,1401 | 0,2162 |
| 2 | 45 | 0,2521 | 0,2444 |
| 3 | 67 | 0,3548 | 0,2985 |
| 4 | 15 | 0,4449 | 0,5333 |
| 5 | 8 | 0,5542 | 0,8750 |
| 6 | 1 | 0,6931 | 1,0000 |
| 7 | 2 | 0,7411 | 1,0000 |
| 8 | 3 | 0,8326 | 0,6667 |
| 9 | 38 | 0,9612 | 0,8947 |

Bin 0 có nhiều mẫu và bám khá sát đường lý tưởng. Các bin 5–8 chỉ có 1–8 mẫu nên dao động lớn và không được overclaim. Bin xác suất cao nhất có xu hướng dự báo cao hơn observed rate. Balanced curve lệch dưới đường lý tưởng ở nhiều bin trung/cao, phù hợp với Brier kém hơn. Không fit Platt/Isotonic trong Week 3.

## 13. Tests trên branch Son

Kết quả `python -m unittest discover -s tests -v` trên branch `Son`:

- Total: 13.
- Passed: 9.
- Failed: 0.
- Skipped: 4.

Chín unit tests chạy trực tiếp gồm tám test data/split Week 2 và một test eligibility của Sơn xác nhận 11 confirmed features loại target, technical và pending features.

`tests/test_son_week3.py` bổ sung bốn assertion còn thiếu:

1. Encoder categories và scaler mean không đổi sau validation prediction.
2. Validation probabilities finite và thuộc [0,1].
3. CV fold không overlap `row_id` hoặc duplicate content.
4. Config ghi `test_evaluated=false` và validation artifacts có đúng validation size.

Các integration test sau được skip có điều kiện, cùng lý do rõ ràng: implementation Week 3 đang ở `origin/Thang` và chưa được tích hợp vào branch `Son`.

- `test_encoder_and_scaler_are_not_refit_during_validation_prediction`
- `test_validation_probabilities_are_finite_and_bounded`
- `test_train_cv_folds_have_no_row_or_duplicate_content_overlap`
- `test_artifacts_explicitly_record_test_as_untouched`

Skip này hợp lệ cho phần cá nhân của Sơn và không bị tính là test failure. Bốn test đã pass khi chạy trên snapshot tạm có code Thắng.

## 14. Dataset provenance/checksum

- Dataset đang dùng: Iranian Churn Dataset.
- Raw file: `data/raw/Customer Churn.csv`, 3.150 dòng.
- Checkout Windows dùng 3.151 CRLF line endings.
- Exact checkout MD5: `e5362c3e5787dadd4e21eb606509bc03`.
- Exact checkout SHA256: `90d5fb6bd1630cd4de4b4d28fcf8b4cb92a8f6ab7484605b0799d47386f7dbe1`, khớp config Week 3 của Thắng.
- Chuẩn hóa đúng CRLF → LF cho cùng bytes tạo MD5 `07311e7080c0fb5b0ce94f5977abc4d5`, khớp checksum tham chiếu được cung cấp; LF SHA256 là `72a4a660cba4166bab4f0c24e930d5453d1917e208c9ce2ed16b841347350dd3`.
- Khác biệt byte-level được giải thích bởi line ending, không phải thay đổi record. Parsing, 3.150 `row_id` và split 1.890/630/630 không đổi; không tạo split mới.
- URL tải gốc, license và citation vẫn chưa có nguồn authoritative trong repository, nên provenance nguồn chưa hoàn toàn đóng.

## 15. Remaining blockers

- `Status` chưa có định nghĩa và availability chính thức.
- `Customer Value` chưa có công thức/calculation window chính thức.
- Source URL, license và citation chưa được xác minh chính thức.
- Candidate vì vậy chỉ là provisional, không phải final model.
- Code/artifact Thắng chưa được tích hợp vào branch chung; việc này không chặn hoàn thành cá nhân của Sơn nhưng cần trước handoff nhóm.

## 16. Handoff cho nhóm / Week 4

Chưa thực hiện Week 4. Trước khi bắt đầu cần:

1. Người phụ trách tích hợp commit Thắng vào branch chung bằng workflow được nhóm phê duyệt.
2. Chạy toàn bộ unit/integration tests sau tích hợp.
3. Review/đóng các vấn đề metadata nếu có nguồn chính thức; nếu feature set thay đổi phải rerun toàn bộ Week 3.
4. Giữ test set đóng cho đến một lần đánh giá cuối theo kế hoạch.
