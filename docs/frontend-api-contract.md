# Frontend ↔ Backend API contract — Week 5

Trạng thái: **PROPOSED / CHỜ THẮNG XÁC NHẬN**. Tại thời điểm audit Week 5, repository chưa có implementation hoặc OpenAPI schema cho `POST /api/churn-score`. Tài liệu này mô tả hợp đồng mà frontend hiện cần; nó không tuyên bố API thật đã tồn tại.

## Endpoint và cấu hình

- Method: `POST`
- Path: `/api/churn-score`
- Content-Type: `application/json`
- Base URL: biến môi trường `VITE_API_BASE_URL`; không hard-code IP máy cá nhân.
- Timeout phía frontend: 10 giây.

## Request đề xuất

```json
{
  "features": {
    "Call  Failure": 1,
    "Complains": 0,
    "Subscription  Length": 24,
    "Charge  Amount": 2,
    "Seconds of Use": 1000,
    "Frequency of use": 80,
    "Frequency of SMS": 12,
    "Distinct Called Numbers": 20,
    "Age Group": 3,
    "Tariff Plan": 1,
    "Status": 1,
    "Age": 35,
    "Customer Value": 42.75
  },
  "capacity_mode": "MEDIUM"
}
```

`capacity_mode` chỉ nhận `LOW`, `MEDIUM`, `HIGH`. Các key feature giữ nguyên tên cột đã đóng băng; ba key `Call  Failure`, `Subscription  Length`, `Charge  Amount` có hai dấu cách ở vị trí thể hiện trong JSON.

Backend phải từ chối field thiếu, giá trị không phải số, `NaN`/vô cực, hoặc giá trị ngoài schema. Frontend không gửi `Churn`, `row_id` hoặc thông tin định danh.

## Response thành công đề xuất

```json
{
  "churn_probability": 0.62,
  "predicted_churn": true,
  "priority_group": "HIGH",
  "threshold": 0.3431830803885034,
  "capacity_mode": "MEDIUM",
  "model_version": "week4-final",
  "request_id": "optional-audit-id"
}
```

Quy ước:

- `churn_probability`: số hữu hạn trong `[0, 1]`.
- `predicted_churn`: kết quả backend khi so với threshold của mode đã chọn.
- `priority_group`: một trong `HIGH`, `MEDIUM`, `EXTENDED`, `NOT_PRIORITIZED`.
- `threshold`: threshold thực tế backend dùng, phải là một trong ba giá trị đóng băng.
- `capacity_mode`: lặp lại mode đã xử lý để frontend kiểm tra/hiển thị nhất quán.
- `model_version`, `request_id`: tùy chọn nhưng nên có cho vận hành và audit.

Frontend hiển thị classification, priority và threshold do API trả về; không thay bằng một bộ logic phân loại khác khi dùng API thật.

## Threshold đóng băng

| Capacity mode | Threshold | Ý nghĩa gốc |
|---|---:|---|
| LOW | 0.47683299575833915 | validation target coverage khoảng 10% |
| MEDIUM | 0.3431830803885034 | validation target coverage khoảng 20%; primary |
| HIGH | 0.16505680661293284 | validation target coverage khoảng 30% |

Các tỷ lệ là mục tiêu xấp xỉ trên validation. Sau refit train + validation, không đảm bảo coverage trên dữ liệu mới chính xác bằng các tỷ lệ này.

## Error contract cần thống nhất

Frontend đã xử lý:

- `400` hoặc `422`: request/validation không hợp lệ;
- `500–599`: lỗi dịch vụ;
- timeout/mất mạng;
- HTTP khác không thành công;
- JSON lỗi hoặc thiếu/sai kiểu các trường response bắt buộc.

Backend nên dùng một body lỗi nhất quán, ví dụ:

```json
{
  "code": "INVALID_FEATURE_VALUE",
  "message": "Input validation failed",
  "details": [
    { "field": "Age Group", "message": "must be between 1 and 5" }
  ]
}
```

Frontend hiện chỉ hiển thị thông báo an toàn theo status; chưa hiển thị trực tiếp `message` từ server để tránh lộ chi tiết nội bộ.

## CORS và triển khai

Nếu frontend và backend khác origin, Thắng cần cấu hình CORS cho đúng origin frontend. Không dùng wildcard credentials trong production. HTTPS, authentication/rate limiting và lưu audit log cần được quyết định ở tầng triển khai, không thuộc phạm vi frontend Week 5.

## Checklist phối hợp với Thắng

- [ ] Xác nhận request dùng object `features` lồng hay flat body.
- [ ] Xác nhận tên key giữ nguyên dấu cách hay backend dùng alias snake_case.
- [ ] Xác nhận enum `capacity_mode` và `priority_group`.
- [ ] Xác nhận backend trả `predicted_churn`, `threshold`, `model_version` và `request_id`.
- [ ] Xác nhận error body và status 400/422.
- [ ] Xác nhận CORS và base URL môi trường tích hợp.
- [ ] Chạy integration/E2E với pipeline thật; tắt `VITE_USE_MOCK_API`.

Cho đến khi checklist hoàn tất, tích hợp API có trạng thái **chờ**, và frontend development chỉ dùng mock được gắn nhãn rõ ràng.
