# Kết quả hỗ trợ triển khai tuần 2 và tuần 3 của Thắng

Ngày chạy: 2026-09-30. Đây là kết quả tạo bằng hỗ trợ AI; Thắng cần đọc code, chạy lại và review với Sơn. Không sửa file gốc của Sơn. Giữ 3.150 dòng, nhóm nội dung trùng theo quy trình của Sơn; split 1.890 train, 630 validation, 630 test. Không chạy dự đoán hoặc tính metric test.

## validation_baselines.csv

| model | AP | ROC_AUC | Brier | precision | recall | F1 |
| --- | --- | --- | --- | --- | --- | --- |
| B0_constant_train_rate | 0.1571 | 0.5000 | 0.1324 | 0.0000 | 0.0000 | 0.0000 |
| B1_logistic_unweighted | 0.7649 | 0.9351 | 0.0707 | 0.8980 | 0.4444 | 0.5946 |

## week3_experiments.csv

| run | class_weight | C | AP_mean | AP_std | ROC_AUC_mean | Brier_mean |
| --- | --- | --- | --- | --- | --- | --- |
| B1_C0.1 | none | 0.1000 | 0.7261 | 0.0765 | 0.9162 | 0.0765 |
| B1_C1 | none | 1.0000 | 0.7357 | 0.0710 | 0.9208 | 0.0740 |
| B1_C10 | none | 10.0000 | 0.7390 | 0.0657 | 0.9226 | 0.0739 |
| M1_C0.1 | balanced | 0.1000 | 0.7214 | 0.0787 | 0.9174 | 0.1235 |
| M1_C1 | balanced | 1.0000 | 0.7274 | 0.0746 | 0.9207 | 0.1195 |
| M1_C10 | balanced | 10.0000 | 0.7306 | 0.0719 | 0.9216 | 0.1195 |

## week3_validation.csv

| model | class_weight | C | AP | ROC_AUC | Brier | precision | recall | F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B1_C1 | none | 1.0000 | 0.7649 | 0.9351 | 0.0707 | 0.8980 | 0.4444 | 0.5946 |
| M1_C1 | balanced | 1.0000 | 0.7599 | 0.9342 | 0.1121 | 0.4531 | 0.8788 | 0.5979 |
| candidate_selected_by_train_CV | none | 10.0000 | 0.7639 | 0.9334 | 0.0707 | 0.8846 | 0.4646 | 0.6093 |

## Diễn giải và giới hạn

B0 không xếp hạng khách hàng: ROC-AUC=0.5, AP bằng tỷ lệ churn validation. Ở ngưỡng 0.5 B0 không dự đoán mẫu dương, precision không xác định; bảng ghi 0 theo quy ước với cờ precision_defined=False.

balanced tăng recall nhưng tăng false positive và Brier ở cùng C=1. Cấu hình ứng viên được chọn từ CV train là logistic không trọng số C=10. Chênh lệch AP giữa các C nhỏ so với biến thiên fold; không coi đó là cải thiện chắc chắn. Chưa chọn ba ngưỡng công suất hoặc hiệu chỉnh xác suất.

13/13 kiểm thử đạt, gồm 8 của Sơn và 5 bổ sung. Pipeline lưu/tải lại được, kể cả khi gặp category mới. Toàn bộ file gốc của Sơn đều giữ nguyên. Quy trình đã chạy lại trên Windows bằng Python 3.13.7; `.venv` có sẵn trong workspace trỏ tới Python của tài khoản khác nên không được dùng.

Manifest trong ZIP ban đầu ghi SHA256 của bản CSV dùng LF. Checkout Windows hiện tại dùng CRLF nên SHA256 theo byte khác dù 3.150 dòng và toàn bộ `row_id` của ba split trùng chính xác với kết quả tạo lại bằng code Sơn. Artifact được cập nhật bằng SHA256 của file thực tế trong checkout này; split không được tạo mới.

Nguồn gốc CSV và định nghĩa/thời điểm biến còn mở theo audit của Sơn. Status và Customer Value bị loại; 11 biến còn lại vẫn có caveat metadata. Kết quả hiện là thử nghiệm tạm thời. Thắng cần bổ sung giờ thực hiện, việc tự kiểm tra và link commit/PR sau khi làm trên máy mình.
