# Dữ liệu dự án: Dự đoán khách hàng rời mạng

## 1. Mục tiêu

Dự án này sử dụng dữ liệu khách hàng viễn thông để dự đoán khả năng một khách hàng sẽ rời mạng trong thời gian tới. Mô hình được xây dựng để hỗ trợ đội chăm sóc khách hàng, ưu tiên kiểm tra các khách hàng có nguy cơ cao và đưa ra các hành động tương ứng.

## 2. Nguồn dữ liệu

Dữ liệu gốc được lưu tại:

- `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`

Tập dữ liệu này mô tả các thuộc tính liên quan đến dịch vụ viễn thông, tài khoản, thói quen sử dụng và trạng thái rời mạng. Dữ liệu nên được lưu ở mức local hoặc ngoài Git nếu đây là dữ liệu có bản quyền hoặc kích thước lớn.

## 3. Cấu trúc dữ liệu

Mỗi dòng trong tập dữ liệu đại diện cho một khách hàng duy nhất. Mỗi khách hàng có các thuộc tính:

- thông tin nhận dạng và hồ sơ tài khoản,
- thông tin dịch vụ đang sử dụng,
- thông tin thanh toán và chi phí,
- trạng thái rời mạng (`Churn`) làm nhãn mục tiêu.

## 4. Mục tiêu mô hình

- Đầu vào: thông tin khách hàng và dịch vụ tại thời điểm quan sát.
- Đầu ra: xác suất khách hàng rời mạng (`Churn`), thường ở dạng nhị phân hoặc xác suất.
- Vai trò: hỗ trợ ra quyết định của đội chăm sóc, không thay thế quyết định con người.

## 5. Mô tả các tập dữ liệu

### data/raw/
Thư mục chứa dữ liệu gốc, chưa qua xử lý. Dữ liệu này thường cần được kiểm tra:

- thiếu dữ liệu,
- giá trị không hợp lệ,
- cột dữ liệu kiểu số/chữ hỗn hợp,
- dữ liệu khuyết thiếu do người dùng hoặc hệ thống.

### data/processed/
Thư mục chứa dữ liệu đã xử lý, ví dụ như:

- `split_indices.json`: chỉ số chia train/validation/test,
- các file đã mã hóa hoặc chuẩn hóa nếu cần.

### data/data_dictionary.csv
Bảng mô tả từng cột dữ liệu, kiểu dữ liệu, ý nghĩa, vai trò trong mô hình và lưu ý xử lý.

## 6. Quy tắc dữ liệu và xử lý

- Không lưu trữ thông tin cá nhân nhạy cảm như số điện thoại, CCCD, email nếu không cần thiết.
- Mã khách hàng (`customerID`) nên được dùng như khóa, không được dùng trực tiếp như feature mô hình nếu không có ý nghĩa phân tích.
- Các biến dạng văn bản cần được mã hóa trong pipeline trước khi huấn luyện.
- Biến tiền tệ và cước phí nên được chuẩn hóa/cast đúng kiểu số.
- Trường `Churn` là nhãn chính để kiểm tra chất lượng mô hình.

## 7. Biến nhãn

- `Churn`: trạng thái khách hàng rời mạng.
  - `Yes`: khách hàng rời mạng
  - `No`: khách hàng còn hoạt động

## 8. Hướng dẫn sử dụng

1. Đặt dữ liệu thô vào `data/raw/`.
2. Kiểm tra dữ liệu bằng pipeline trong `src/data.py`.
3. Cập nhật `data/data_dictionary.csv` nếu có thêm/bớt cột.
4. Tạo feature và tiền xử lý trong `src/features.py`.
5. Huấn luyện và đánh giá mô hình trong `src/train.py` và `src/evaluate.py`.
6. Lưu mô hình, kết quả và báo cáo ra `models/` và `reports/`.

## 9. Lưu ý

- Nếu dữ liệu là dữ liệu thực tế, cần kiểm tra quyền sử dụng, bảo mật và tuân thủ pháp luật.
- Nếu repo dùng môi trường học tập, nên ưu tiên dữ liệu demo hoặc dữ liệu công khai có giấy phép rõ ràng.
- Mục tiêu của dự án là hỗ trợ ra quyết định, không thay thế quyền kiểm soát của con người.
