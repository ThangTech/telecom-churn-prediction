# Phần tuần 2 và tuần 3 của Thắng

Bộ mã này bổ sung phần baseline và thí nghiệm vào bản Sơn đã sửa. Các file sẵn có của Sơn được giữ nguyên. Kết quả hiện là thử nghiệm tạm thời: nguồn gốc CSV và một số định nghĩa/thời điểm biến chưa được xác minh đầy đủ theo `reports/leakage-audit.md`.

## Chạy trong PowerShell tại thư mục gốc dự án

Nếu đã có môi trường Python với các thư viện trong requirements.txt thì dùng môi trường đó. Nếu chưa có:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Tuần 2:

```powershell
.\.venv\Scripts\python.exe scripts/prepare_splits.py
.\.venv\Scripts\python.exe scripts/train_baselines.py
```

Tuần 3, sau khi đọc và hiểu kết quả tuần 2:

```powershell
.\.venv\Scripts\python.exe scripts/run_experiments.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Nếu đang kích hoạt môi trường ảo, có thể thay `.\.venv\Scripts\python.exe` bằng `python`. Không sao chép môi trường ảo của người khác.

## Tuần 2 đã triển khai

- Đọc và làm sạch bằng hàm của Sơn, không loại dòng bổ sung.
- Giữ split xấp xỉ 60/20/20 theo nhóm nội dung trùng của Sơn; lưu row_id, seed, SHA256 và phiên bản scikit-learn trong `data/processed/split_indices.json`.
- B0 gán xác suất bằng tỷ lệ churn trên train cho mọi dòng validation.
- B1 dùng Logistic Regression không class_weight, C=1. Tiền xử lý nằm trong Pipeline.
- Median/most-frequent imputer, StandardScaler và OneHotEncoder đều fit trên train. Complains, Age Group, Tariff Plan được xử lý như danh mục; các biến số còn lại được scale. Đây là lựa chọn triển khai cần nhóm review, không phải xác nhận ý nghĩa cột từ nguồn UCI.
- Không dùng Churn, row_id, Status hoặc Customer Value làm đặc trưng. Hai biến cuối chờ xác minh.

## Tuần 3 đã triển khai

- So sánh C=1 giữa class_weight=None và balanced để thấy riêng tác động trọng số lớp.
- Tìm cấu hình trong sáu tổ hợp: C thuộc 0.1, 1, 10; class_weight thuộc None, balanced.
- CV 5 fold chỉ trên train, cùng fold cho tất cả cấu hình; nhóm dòng trùng không vượt ranh giới fold. Mỗi fold tạo và fit lại cả Pipeline.
- Chọn cấu hình theo AP trung bình CV cao nhất; nếu bằng điểm, dùng thứ tự cấu hình công bố. Validation chỉ báo kết quả sau chọn, không chọn lại cấu hình theo điểm validation.
- Lưu mô hình ứng viên fit trên train, biểu đồ calibration và ma trận nhầm lẫn validation. Chưa fit lại trên train+validation, chưa đánh giá test, chưa chọn ba ngưỡng công suất cho tuần 4.

## Đọc kết quả

`reports/validation_baselines.csv` chứa B0 và B1. `reports/week3_experiments.csv` chứa trung bình/độ lệch chuẩn mẫu qua fold; `reports/week3_cv_folds.csv` chứa từng fold; `reports/week3_validation.csv` chứa so sánh validation. `reports/week3_calibration_bins.csv` có số mẫu mỗi bin; bin ít mẫu khiến đường calibration dao động lớn.

AP là Average Precision, không phải PR-AUC tích phân hình thang. Brier thấp hơn tốt hơn. Ngưỡng phân loại tạm thời là 0.5. Nếu không dự đoán mẫu dương, precision được ghi 0 theo quy ước và `precision_defined=False`, không diễn giải như một precision đo được.

Với ngưỡng 0.5, class_weight balanced có thể tăng recall nhưng tăng số báo động nhầm và làm xác suất kém calibration. Nó không mặc định tốt hơn.

## Việc nhóm vẫn phải làm

Xác minh nguồn tải, giấy phép, định nghĩa và thời điểm biến; giải thích hai checksum khác nhau trong hồ sơ. Chưa tuyên bố pipeline đã loại trừ mọi rò rỉ khi các thông tin này còn mở. Grouping theo nội dung không chứng minh đã chia theo khách hàng thật vì CSV không có mã khách hàng. Không xem/sử dụng kết quả test để sửa mô hình.

Các file được tạo bằng hỗ trợ AI. Thắng và Sơn cần đọc code, chạy lại trên máy mình, review quyết định và ghi phạm vi hỗ trợ vào hồ sơ AI của nhóm; không ghi rằng đã tự viết hoặc kiểm chứng những phần chưa làm.

## Đưa phần mới vào repo

Tạo nhánh riêng và chỉ chép các file mới từ `thang-week2-week3-additions.zip`. Sau khi chạy thành công, dùng `git status` để xem thay đổi và review cùng Sơn trước khi merge. Các pipeline joblib có thể tái tạo bằng script; chỉ nạp artifact do nhóm tạo từ nguồn tin cậy. Không commit .venv hoặc cache.
