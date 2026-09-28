# Backlog dự án: Dự đoán khách hàng rời mạng

## 1. Mục tiêu sản phẩm

Xây dựng hệ thống hỗ trợ dự đoán nguy cơ khách hàng viễn thông rời mạng, giúp đội chăm sóc khách hàng tập trung vào những khách hàng có rủi ro cao. Hệ thống gồm một pipeline phân loại, các báo cáo đánh giá và một giao diện web để nhập dữ liệu hoặc tải CSV và xem kết quả dự đoán.

## 2. Các epic chính

### Epic 1: Thu thập và chuẩn hóa dữ liệu
- Thu thập dữ liệu khách hàng viễn thông từ nguồn đáng tin cậy.
- Kiểm tra schema, kiểu dữ liệu và dữ liệu thiếu.
- Xây dựng data dictionary cho từng cột.
- Lưu dữ liệu raw và processed theo quy chuẩn của dự án.

### Epic 2: Xây dựng pipeline mô hình
- Tiền xử lý dữ liệu: xử lý thiếu dữ liệu, mã hóa category, chuẩn hóa số.
- Chia tập train/validation/test.
- Huấn luyện baseline và mô hình chính.
- Ghi lại độ đo: precision, recall, F1, PR-AUC, ROC-AUC.

### Epic 3: Đánh giá và tối ưu hóa
- So sánh mô hình baseline và mô hình thực tế.
- Đánh giá theo ngưỡng phù hợp với hoạt động chăm sóc khách hàng.
- Phân tích lỗi mô hình và phân nhóm khách hàng có nguy cơ cao.
- Viết báo cáo và hình ảnh minh họa.

### Epic 4: Tạo giao diện web và API
- Tạo backend API để nhận dữ liệu đầu vào.
- Tạo frontend để người dùng nhập dữ liệu hoặc tải file CSV.
- Hiển thị xác suất churn và mức độ ưu tiên.
- Chạy kiểm thử cơ bản cho luồng dự đoán.

## 3. Backlog công việc

### Mức ưu tiên cao
- [ ] Hoàn thiện `data/README.md` và `data/data_dictionary.csv`
- [ ] Kiểm tra dữ liệu raw và xác định schema cuối cùng
- [ ] Xây dựng pipeline tiền xử lý dữ liệu
- [ ] Huấn luyện mô hình baseline
- [ ] Tạo API dự đoán `POST /api/churn-score`
- [ ] Thiết kế giao diện người dùng màn hình dự đoán

### Mức ưu tiên trung bình
- [ ] So sánh các mô hình và chọn mô hình tốt hơn
- [ ] Tạo dashboard hiển thị kết quả
- [ ] Tạo báo cáo bằng file CSV và hình ảnh
- [ ] Hoàn thiện kiểm thử cho pipeline

### Mức ưu tiên thấp
- [ ] Cải thiện UX trên frontend
- [ ] Thêm mô tả model card / giải thích mô hình
- [ ] Tích hợp lưu lịch sử dự đoán hoặc audit log

## 4. Phác thảo luồng web

### 4.1 Màn hình 1: Trang chủ / Giới thiệu
- Hiển thị tên dự án: Dự đoán khách hàng rời mạng.
- Mô tả mục tiêu, lợi ích và cách sử dụng.
- Nút “Bắt đầu” hoặc “Dự đoán ngay”.

### 4.2 Màn hình 2: Nhập dữ liệu hoặc tải CSV
- Người dùng có thể:
  - nhập thủ công các trường như tenure, contract, monthly charges, payment method,
  - hoặc tải file CSV chứa dữ liệu khách hàng.
- Hệ thống kiểm tra: kiểu dữ liệu, thiếu trường, giá trị không hợp lệ.
- Nếu có lỗi, hiển thị thông báo rõ ràng và yêu cầu sửa lại.

### 4.3 Màn hình 3: Xử lý và dự đoán
- Frontend gửi dữ liệu tới backend API.
- Backend:
  - kiểm tra đầu vào,
  - áp dụng pipeline tiền xử lý,
  - gọi mô hình đã huấn luyện,
  - trả kết quả xác suất churn.
- API có thể trả về JSON:

```json
{
  "customer_id": "CUST-001",
  "probability_churn": 0.82,
  "risk_level": "Cao",
  "recommended_action": "Tiếp cận sớm và tư vấn khuyến mãi"
}
```

### 4.4 Màn hình 4: Kết quả và dashboard
- Hiển thị xác suất churn theo từng khách hàng.
- Phân nhóm mức nguy cơ: Thấp / Trung bình / Cao.
- Hiển thị danh sách khách hàng ưu tiên chăm sóc.
- Cho phép xem chi tiết từng bản ghi và giải thích yếu tố ảnh hưởng đến kết quả.

### 4.5 Màn hình 5: Báo cáo và model card
- Cung cấp các số liệu đánh giá: precision, recall, F1, PR-AUC.
- Hiển thị mô hình đang dùng và các ngưỡng cảnh báo.
- Cung cấp danh mục yếu tố chính ảnh hưởng đến nguy cơ churn.

## 5. Tiêu chí chốt dự án

- Tập dữ liệu có data dictionary rõ ràng.
- Pipeline xử lý dữ liệu chạy được trên môi trường mới.
- Mô hình dự đoán có báo cáo đánh giá minh bạch.
- Frontend và backend giao tiếp ổn định.
- Luồng dự đoán dễ dùng cho người không chuyên về machine learning.

## 6. Ghi chú

Đây là backlog giai đoạn đầu của dự án, có thể cập nhật theo từng sprint. Mục tiêu cuối cùng không chỉ là xây dựng mô hình tốt, mà còn đảm bảo hệ thống có thể được triển khai và dùng trực tiếp trong hoạt động chăm sóc khách hàng.
