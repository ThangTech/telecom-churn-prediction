# Week 5 — Sơn — Frontend dự đoán churn

## Mục tiêu

Xây dựng frontend độc lập cho đề tài Dự đoán khách hàng viễn thông rời mạng: giới thiệu bài toán, nhập đúng 13 feature, hiển thị kết quả, dashboard demo an toàn và Model Card. Không huấn luyện lại model, không đọc/chạy lại test set và không triển khai backend thay cho Thắng.

## Audit trước triển khai

- Repository chưa có ứng dụng frontend; thư mục `web/` chưa tồn tại.
- Repository chưa có implementation hoặc OpenAPI contract cho `POST /api/churn-score`; backlog vẫn ghi API là TODO.
- Feature set Week 4 ở trạng thái FINAL gồm 13 feature: Call Failure, Complains, Subscription Length, Charge Amount, Seconds of Use, Frequency of use, Frequency of SMS, Distinct Called Numbers, Age Group, Tariff Plan, Status, Age, Customer Value.
- Frozen thresholds: LOW `0.476833`, MEDIUM `0.343183`, HIGH `0.165057`; MEDIUM là primary.
- Schema nhập liệu chỉ dùng miền đã ghi trong `data/data_dictionary.csv`; không tự đặt cận trên khi tài liệu chỉ quy định `>=0`.
- Các file model, config, dữ liệu processed và report Week 2–4 không được sửa.

## Phạm vi Sơn đã triển khai

- React + TypeScript + Vite tại `web/`.
- Route giới thiệu với mục tiêu, Iranian Churn Dataset, Logistic Regression và cửa sổ 9 + 3 tháng.
- Form đủ 13 feature, nhãn tiếng Việt, tên gốc, đơn vị, select cho danh mục, validation required/kiểu/miền tại từng trường.
- Không có `Churn`, `row_id`, số điện thoại hoặc trường thông tin định danh.
- Cho phép chọn ba mode công suất bằng đúng frozen thresholds; cảnh báo công suất không phải mức nguy cơ.
- Kết quả gồm probability, classification, priority, threshold, cách diễn giải và cảnh báo xác suất không phải kết luận.
- Dashboard với mã khách hàng giả, sắp xếp xác suất giảm dần, lọc nhóm, bảng và biểu đồ phân bố có đơn vị/chú thích.
- Model Card phân biệt validation/test metrics, mô tả intended use, not intended use, threshold protocol và limitations.
- Responsive cho desktop, tablet và mobile; hỗ trợ reduced-motion.

## Tích hợp API

Trạng thái: **CHỜ BACKEND CỦA THẮNG — CHƯA E2E**.

Frontend có kiểu request/response tại `web/src/types/churn.ts`, service tại `web/src/services/churnApi.ts` và hợp đồng đề xuất tại `docs/frontend-api-contract.md`. Base URL lấy từ `VITE_API_BASE_URL`.

Khi chạy development và đặt `VITE_USE_MOCK_API=true`, frontend trả một response minh họa cố định, gắn nhãn **DỮ LIỆU MÔ PHỎNG**. Mock không chạy trong production và không chứa/không mô phỏng model ở frontend.

Frontend xử lý thiếu/sai field, 400/422, 500, HTTP khác, timeout 10 giây, lỗi mạng, JSON/response sai schema, loading và chống gửi trùng.

## File tạo mới

- `web/**`: cấu hình ứng dụng, source, style, test và hướng dẫn chạy.
- `docs/frontend-api-contract.md`: hợp đồng tích hợp cần Thắng xác nhận.
- `docs/weekly/week-05-son.md`: nhật ký này.

Không sửa file dùng chung, artifact mô hình, frozen config, split hoặc report Week 2–4.

## Kiểm thử

Các case tự động gồm:

1. trang giới thiệu render;
2. form có đúng 13 feature;
3. dữ liệu thiếu/sai bị chặn;
4. dữ liệu hợp lệ chuyển thành request đúng schema;
5. probability và priority từ mock response hiển thị đúng;
6. loading và chống gửi trùng;
7. API lỗi không làm crash;
8. dashboard ghi rõ dữ liệu demo không phải test;
9. Model Card dùng metric đóng băng;
10. response API sai schema và HTTP 422 được xử lý.

Kết quả xác minh local ngày 2026-10-01:

- `npm run lint`: **PASS**.
- `npm run test`: **PASS — 6 test files, 13/13 test cases**.
- `npm run build`: **PASS — Vite production build hoàn tất**.
- `npm audit --omit=dev`: **0 production vulnerabilities** sau khi dùng React Router 7.18.4.
- Kiểm tra trực quan local: **PASS** cho trang giới thiệu, form, dashboard và Model Card ở viewport hẹp; navigation, phân cấp nội dung và responsive layout hiển thị đúng.

Không chạy bất kỳ test Python/model/test-set evaluation nào trong quá trình này.

## Vấn đề còn tồn tại và phối hợp

- Thắng cần xác nhận nesting/key alias, enum, error body, CORS và các field response theo checklist trong API contract.
- Chưa thể tuyên bố tích hợp end-to-end trước khi API thật được bàn giao và integration test chạy thành công.
- Cần kiểm tra mapping feature và pipeline backend bằng một request fixture chung; không sử dụng test set để làm fixture demo.
- Thời gian thực hiện: **chưa ghi nhận** vì Sơn chưa cung cấp số giờ; không tự ước lượng thay Sơn.

## Cam kết Week 4

Không retrain, không chạy CV/model selection, không đánh giá lại test, không đổi seed/split/13-feature set/C/class_weight/threshold và không dùng dữ liệu test cho dashboard.
