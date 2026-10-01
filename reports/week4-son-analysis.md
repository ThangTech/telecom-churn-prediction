# Week 4 Analysis — Sơn

Phạm vi: hoàn tất thí nghiệm, freeze feature/model/threshold, đánh giá test đúng một lần, phân tích calibration, coefficient và lỗi. Không làm API/Web hoặc Week 5. Không merge/cherry-pick/commit/push.

## Correction 1 — 13-feature CV verification

**CV RERUN AFTER 13-FEATURE CHANGE: YES.** Sau khi thêm Status và Customer Value, Week 3 đã chạy lại đủ sáu cấu hình class_weight ∈ {None, balanced} × C ∈ {0.1, 1, 10}. Artifact có 30 fold rows = 6 runs × 5 folds, dùng train only và seed 42. Config ghi 13 features. Isolated runner snapshot tạo một danh sách folds duy nhất trước vòng lặp cấu hình; mỗi fold fit một pipeline mới, nên imputer/scaler/encoder chỉ học fold-train và cùng folds được dùng cho mọi cấu hình.

| Run | PR_AUC mean ± std | AP mean ± std | ROC_AUC mean ± std | Brier mean ± std | Precision mean | Recall mean | F1 mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| None, C=0.1 | 0.726344 ± 0.068166 | 0.729622 ± 0.066907 | 0.924767 ± 0.020072 | 0.075001 ± 0.009366 | 0.834756 | 0.404181 | 0.534608 |
| None, C=1 | 0.742968 ± 0.067981 | 0.745753 ± 0.067056 | 0.929018 ± 0.020216 | 0.072627 ± 0.011074 | 0.806210 | 0.441186 | 0.560666 |
| None, C=10 | **0.752463 ± 0.069578** | **0.755157 ± 0.068643** | 0.931712 ± 0.020389 | 0.071827 ± 0.011535 | 0.768423 | 0.444689 | 0.556367 |
| balanced, C=0.1 | 0.718777 ± 0.067492 | 0.722202 ± 0.066302 | 0.926279 ± 0.019730 | 0.114568 ± 0.015849 | 0.479968 | 0.885650 | 0.621480 |
| balanced, C=1 | 0.737933 ± 0.071805 | 0.740859 ± 0.070755 | 0.930645 ± 0.020414 | 0.111111 ± 0.016441 | 0.492276 | 0.885650 | 0.631505 |
| balanced, C=10 | 0.745701 ± 0.070387 | 0.748578 ± 0.069352 | 0.932734 ± 0.019720 | 0.109759 ± 0.016108 | 0.501809 | 0.889040 | 0.640494 |

Theo rule highest mean train-CV PR_AUC, candidate được chọn lại từ chính CV 13-feature là class_weight=None, C=10. Không dùng kết quả CV 11-feature để biện minh cho candidate này.

## Correction 2 — Temporal audit: Status

- Definition: subscription status, 1=active và 2=non-active.
- Official timing: UCI ghi mọi non-target attribute là aggregate của chín tháng đầu; churn label ở cuối tháng 12 và có planning gap ba tháng.
- Availability: có trước prediction point theo metadata chính thức.
- Outcome use: UCI tách Churn thành class label riêng; không có bằng chứng Status dùng outcome tháng 12.

**STATUS DECISION: KEEP.** Quyết định dựa trên official temporal metadata, không dựa trên correlation.

## Correction 3 — Temporal audit: Customer Value

- Official definition: calculated value of customer.
- Official timing: UCI đặt biến trong nhóm non-target attributes được aggregate từ chín tháng đầu.
- Formula/component fields: không được công bố trên UCI page.
- Future/outcome evidence: UCI gọi Customer Value là non-target attribute, liệt kê nó trong 13 input attributes và xác nhận mọi non-target attribute được aggregate trong chín tháng đầu, trước churn label tháng 12. Không có bằng chứng biến dùng Churn/outcome.

**CUSTOMER VALUE DECISION: KEEP.** Temporal availability dựa trên official UCI observation-window description. Exact formula unknown được ghi là limitation; thiếu formula không được coi là bằng chứng leakage.

## Correction 4 — Final feature-set decision

Status và Customer Value đều KEEP dựa trên official UCI temporal metadata. Artifact đã đánh giá chứa đúng 13 features và Week 3 đã rerun đầy đủ 6 configurations × 5 folds sau thay đổi. **FEATURE SET STATUS: FINAL.** Không thay feature/model và không rerun test trong correction này.

## Correction 5 — Threshold/refit protocol review

Quy trình đã dùng đúng là:

1. Model A fit train.
2. Chọn thresholds 10%/20%/30% từ probabilities của validation.
3. Freeze threshold chính 0.343183.
4. Model B cùng hyperparameters fit lại train+validation.
5. Áp nguyên absolute threshold lên test.

Không có test tuning. Refit có thể đổi probability scale/calibration, nên 0.343183 không được diễn giải là bảo đảm đúng capacity 20% trên mọi dataset. Ba thresholds được chọn trên validation để tương ứng validation target coverage khoảng 10%/20%/30%; sau final refit, realized coverage trên test/new data chỉ là approximate. Threshold đã freeze trước test và không được chỉnh theo test. **THRESHOLD VALIDITY: VALID AS FROZEN; CAPACITY INTERPRETATION APPROXIMATE AFTER REFIT.**

## Correction 6 — Test contamination check

Test đã được mở đúng một final reporting event; count vẫn là 1 và không reset. Không có bằng chứng test được dùng để chọn feature, C, class_weight hoặc threshold, và audit này không chạy lại test.

Không có quyết định feature, model, C, class_weight hoặc threshold nào được thay đổi dựa trên test. Correction này chỉ sửa metadata và cách diễn giải; không mở test thêm lần nào. **TEST CONTAMINATION: NONE FOR THE REPORTED FROZEN EVALUATION.** Việc realized capacity sau refit chỉ xấp xỉ là protocol limitation, không phải test leakage.

## Correction 7 — Baseline PR_AUC caveat

B0 constant scorer có AP=0.157143, đúng bằng development prevalence, và ROC_AUC=0.5, thể hiện không có ranking ability. Trapezoidal PR_AUC=0.578571 cao bất thường vì degenerate constant-score precision-recall curve có endpoint geometry; con số này không chứng minh baseline ranking tốt. PR_AUC vẫn được giữ trong bảng theo yêu cầu, nhưng AP và ROC_AUC là hai tham chiếu dễ diễn giải hơn cho B0.

## 1. Mục tiêu Week 4

Hoàn thiện phần Sơn theo đề: bảng kết quả đóng băng, ba ngưỡng theo công suất chăm sóc, final test evaluation, figures, coefficient/error analysis và model card nháp. Test không được dùng để chọn feature, preprocessing, C, class_weight hoặc threshold.

## 2. Feature freeze

FEATURE SET STATUS: FINAL.

Frozen 13 features: Call Failure, Complains, Subscription Length, Charge Amount, Seconds of Use, Frequency of use, Frequency of SMS, Distinct Called Numbers, Age Group, Tariff Plan, Status, Age, Customer Value.

UCI metadata xác nhận mọi non-target attribute được tổng hợp trong chín tháng đầu. Status và Customer Value đều KEEP; exact Customer Value formula không được công bố và được giữ như limitation, không phải leakage evidence. Churn là target; row_id là technical. Freeze timestamp: 2026-09-30T15:01:54Z. Snapshot: origin/Thang@7e3be82d cộng Week 3 assignment-aligned working tree trên Son head 3e04db76b1fb.

## 3. Model freeze

- Model: LogisticRegression.
- class_weight: None.
- C: 10.
- seed: 42.
- Primary selection metric: mean train-CV PR_AUC.
- Selection source: five-fold StratifiedGroupKFold trên train only.
- Final fit: train+validation, chỉ sau khi freeze.
- Numeric preprocessing: median imputer + StandardScaler.
- Categorical preprocessing: most-frequent imputer + OneHotEncoder(handle_unknown="ignore").

Không thay model sau khi xem test.

## 4. Threshold design

Không dùng các ngưỡng tùy ý 0.3/0.5/0.7. Candidate train-fit được dự đoán trên validation và probability cut-off được lấy theo top capacity:

- LOW: liên hệ khoảng 10% khách hàng, ưu tiên precision.
- MEDIUM: khoảng 20%, cân bằng khả năng phát hiện và workload.
- HIGH: khoảng 30%, ưu tiên recall.

Nếu nhiều khách có cùng probability tại cut-off, actual coverage có thể lệch nhẹ do không tách tie.

## 5. Three capacity thresholds

| Capacity | Frozen threshold | Validation contacts | Coverage | Precision | Recall | F1 | FP | FN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| LOW | 0.476833 | 63 | 10.00% | 0.761905 | 0.484848 | 0.592593 | 15 | 51 |
| MEDIUM | 0.343183 | 126 | 20.00% | 0.595238 | 0.757576 | 0.666667 | 51 | 24 |
| HIGH | 0.165057 | 190 | 30.16% | 0.468421 | 0.898990 | 0.615917 | 101 | 10 |

Primary threshold là MEDIUM, 0.343183, vì giả định đội chăm sóc xử lý khoảng 20% khách hàng.

## 6. Validation threshold analysis

LOW giảm workload và tăng precision nhưng bỏ sót 51/99 churn. MEDIUM tăng recall lên 0.758 và có F1 cao nhất trong ba operating points validation. HIGH phát hiện gần 90% churn nhưng tạo 101 false positives. Lựa chọn MEDIUM được đóng băng trước test vì cân bằng coverage 20%, không phải vì kết quả test.

Ranking metrics của candidate trên validation: PR_AUC 0.760070, AP 0.761101, ROC_AUC 0.936493, Brier 0.069941.

## 7. Frozen evaluation protocol

Trước test, configs/week4_frozen_evaluation.json ghi:

- raw SHA256, split manifest checksum và seed;
- 13 features và preprocessing;
- model type, class_weight=None, C=10;
- three capacity thresholds và primary threshold;
- grouping boundaries cho Subscription Length và Charge Amount;
- test_evaluated=false, test_evaluation_count=0.

Preflight chỉ dùng development data và đã pass. Final script đổi trạng thái sang test_evaluation_started trước prediction, nên guard ngăn chạy lại nếu có lỗi. Sau khi hoàn tất: test_evaluated=true, count=1, decisions_changed_after_evaluation=false.

## 8. Final test evaluation

Pipeline fit trên train+validation sau khi hyperparameters và thresholds đã freeze, rồi được đánh giá test đúng một lần tại threshold chính 0.343183. Correction audit không thay đổi hoặc chạy lại các số dưới đây.

| Metric | Value |
|---|---:|
| PR_AUC | 0.796582 |
| AP | 0.798105 |
| ROC_AUC | 0.949951 |
| Brier | 0.062798 |
| Precision | 0.678261 |
| Recall | 0.787879 |
| F1 | 0.728972 |
| Predicted positive | 115 |
| TN | 494 |
| FP | 37 |
| FN | 21 |
| TP | 78 |

Không có quyết định nào được đổi theo kết quả này.

Test results tại ba threshold đã freeze:

| Capacity | Test coverage | Precision | Recall | F1 | TN | FP | FN | TP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| LOW | 11.27% | 0.732394 | 0.525253 | 0.611765 | 512 | 19 | 47 | 52 |
| MEDIUM | 18.25% | 0.678261 | 0.787879 | 0.728972 | 494 | 37 | 21 | 78 |
| HIGH | 26.98% | 0.517647 | 0.888889 | 0.654275 | 449 | 82 | 11 | 88 |

Coverage test khác validation là hành vi bình thường của frozen probability cut-off; không được chỉnh threshold theo test.

## 9. Confusion matrix

Tại primary threshold:

- TP=78: khách churn được phát hiện đúng và có thể được ưu tiên chăm sóc.
- FP=37: khách không churn vẫn được đưa vào danh sách, tạo workload không cần thiết.
- FN=21: khách churn bị bỏ sót, là chi phí nghiệp vụ quan trọng.
- TN=494: khách không churn được nhận diện đúng.

So với threshold 0.5, threshold capacity-based ưu tiên recall phù hợp mục tiêu giữ chân nhưng vẫn giữ workload gần mức 20%.

## 10. Calibration

Test Brier score là 0.062798.

| Bin | n | Mean probability | Observed churn |
|---:|---:|---:|---:|
| 0 | 410 | 0.0181 | 0.0049 |
| 1 | 67 | 0.1471 | 0.1791 |
| 2 | 29 | 0.2476 | 0.1724 |
| 3 | 35 | 0.3668 | 0.5143 |
| 4 | 25 | 0.4547 | 0.6000 |
| 5 | 17 | 0.5464 | 0.2941 |
| 6 | 3 | 0.6432 | 0.3333 |
| 7 | 3 | 0.7551 | 0.6667 |
| 8 | 7 | 0.8840 | 0.8571 |
| 9 | 34 | 0.9565 | 0.9706 |

Bin 0 hơi overpredict; bin 3–4 underpredict; bin 5 overpredict. Bins 6–8 quá nhỏ để kết luận. Không recalibrate sau khi xem test.

## 11. Coefficient analysis

Top positive:

- Customer Value: +3.3239.
- Age Group_2: +1.5363.
- Complains_1: +1.5111.
- Age Group_3: +1.2700.
- Call Failure: +0.9759.

Top negative:

- Frequency of SMS: −4.4863.
- Frequency of use: −2.9767.
- Age Group_1: −2.7477.
- Complains_0: −2.3252.
- Age Group_5: −1.7249.

Positive/negative chỉ mô tả liên hệ với log-odds dự đoán, không phải tác động nhân quả. Numeric coefficients tương ứng thay đổi một standard deviation. Correlated features và full one-hot levels làm coefficient riêng lẻ cần được diễn giải thận trọng.

## 12. Error analysis by Subscription Length

Boundaries 32 và 37 được fit từ train+validation predictors trước test.

| Group | n | Churn rate | Precision | Recall | F1 | FP | FN |
|---|---:|---:|---:|---:|---:|---:|---:|
| low, ≤32 | 218 | 0.1147 | 0.4615 | 0.7200 | 0.5625 | 21 | 7 |
| medium, 32–37 | 225 | 0.2089 | 0.8333 | 0.8511 | 0.8421 | 8 | 7 |
| high, >37 | 187 | 0.1444 | 0.7143 | 0.7407 | 0.7273 | 8 | 7 |

Low tenure có precision thấp và nhiều FP nhất. Mỗi group có bảy FN. Kết quả mô tả sự khác biệt của model, không chứng minh tenure gây churn.

## 13. Error analysis by Charge Amount

Boundaries 0 và 1 được fit trước test.

| Group | n | Churn rate | Precision | Recall | F1 | FP | FN |
|---|---:|---:|---:|---:|---:|---:|---:|
| low, ≤0 | 340 | 0.2412 | 0.6571 | 0.8415 | 0.7380 | 36 | 13 |
| medium, 0–1 | 136 | 0.0588 | 0.8000 | 0.5000 | 0.6154 | 1 | 4 |
| high, >1 | 154 | 0.0584 | 1.0000 | 0.5556 | 0.7143 | 0 | 4 |

Low-charge group lớn và có churn prevalence cao hơn nên chứa phần lớn absolute errors. Medium/high chỉ có 8–9 churn cases mỗi group; recall của chúng không ổn định và không nên overclaim.

## 14. Baseline comparison

Mọi dòng dưới đây đều được fit trên development và đánh giá trên cùng frozen test trong một final reporting event:

| Model | Threshold | PR_AUC | AP | ROC_AUC | Brier | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B0 constant rate | 0.5 | 0.578571 | 0.157143 | 0.500000 | 0.132449 | 0.000000 | 0.000000 | 0.000000 |
| B1 Logistic C=1 | 0.5 | 0.795103 | 0.796707 | 0.950446 | 0.063204 | 0.771930 | 0.444444 | 0.564103 |
| Final Logistic C=10 | 0.343183 | 0.796582 | 0.798105 | 0.949951 | 0.062798 | 0.678261 | 0.787879 | 0.728972 |

C=1 và C=10 có ranking/calibration gần nhau. Khác biệt classification lớn chủ yếu phản ánh threshold đã freeze khác nhau; không dùng bảng test để chọn lại C hay threshold. Trapezoidal PR_AUC của constant score chịu ảnh hưởng endpoint geometry, nên AP=prevalence và ROC_AUC=0.5 là baseline ranking dễ diễn giải hơn.

## 15. Limitations

- Dataset chỉ có 3.150 bản ghi và một nguồn/population.
- Exact Customer Value formula chưa có trên public UCI page.
- Một số calibration/group bins nhỏ.
- Threshold capacity có thể drift khi phân phối xác suất thay đổi.
- Charge Amount có ít mức và tertile grouping tạo groups không cân bằng.
- Coefficients không phải quan hệ nhân quả.
- Chưa có fairness audit đầy đủ.
- Test đã dùng một lần và không được dùng cho tuning tiếp theo.
- Exact Customer Value formula không được công bố; đây là limitation, không phải bằng chứng leakage.
- Absolute threshold được chọn từ train-fit validation probabilities rồi áp dụng sau train+validation refit; realized capacity là approximate, không được bảo đảm chính xác 10%/20%/30%.

## 16. Model card summary

docs/model-card-draft.md đã được cập nhật với 13-feature set FINAL, Customer Value formula limitation, frozen threshold protocol và realized-capacity caveat sau refit.

## 17. Week 5 handoff

Week 4 correction status là **PASS** và sẵn sàng Week 5. Handoff có frozen config, final model/test tables, six figures, coefficients/error reports, model card và tests. Correction suite trên branch Sơn: 27 total, 23 passed, 0 failed, 4 conditional skips. Không được tune tiếp bằng test đã mở; threshold capacity được diễn giải là approximate sau refit.
