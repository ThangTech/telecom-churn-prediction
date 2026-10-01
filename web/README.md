# Week 5 frontend — Telecom Churn Prediction

Ứng dụng React + TypeScript + Vite do Sơn phụ trách. Frontend không chứa model và không triển khai backend thay cho phần của Thắng.

## Chạy local

Yêu cầu Node.js 20 trở lên.

```powershell
cd web
npm install
Copy-Item .env.example .env.local
npm run dev
```

Mặc định file mẫu bật `VITE_USE_MOCK_API=true`. Mock chỉ hoạt động với Vite development server và mọi kết quả mock đều có nhãn **DỮ LIỆU MÔ PHỎNG**. Production build luôn gọi API thật.

Để tích hợp backend:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK_API=false
```

Frontend gọi `POST /api/churn-score`. Hợp đồng đề xuất và các điểm cần Thắng xác nhận nằm tại `docs/frontend-api-contract.md`.

## Kiểm tra

```powershell
npm run lint
npm run test
npm run build
```

Các route:

- `/`: giới thiệu bài toán và cửa sổ quan sát;
- `/predict`: form 13 feature, chọn công suất và kết quả;
- `/dashboard`: dữ liệu demo an toàn, không lấy từ test;
- `/model-card`: metric, threshold và giới hạn đã công bố ở Week 4.

## Quy tắc dữ liệu

- Không nhập `Churn` hoặc `row_id`.
- Không nhập họ tên, số điện thoại thật hoặc địa chỉ.
- Tên key request giữ nguyên tên cột gốc, bao gồm hai dấu cách trong `Call  Failure`, `Subscription  Length` và `Charge  Amount`.
- Frontend chỉ xác thực các miền có bằng chứng trong `data/data_dictionary.csv`; không tự đặt cận trên cho trường chỉ được định nghĩa là `>=0`.
