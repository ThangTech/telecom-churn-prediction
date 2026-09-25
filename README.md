# PROJECT 15 - Dự đoán khách hàng viễn thông rời mạng
# test commit
## Giới thiệu

Dự án xây dựng quy trình dự đoán khả năng khách hàng viễn thông rời mạng
(customer churn). Quy trình dự kiến bao gồm chuẩn bị dữ liệu, tạo đặc trưng,
huấn luyện mô hình, đánh giá và cung cấp dự đoán qua API.

## Cấu trúc dự án

| Đường dẫn                  | Nội dung                                                                  |
| -------------------------- | ------------------------------------------------------------------------- |
| `data/`                    | Dữ liệu thô, dữ liệu đã xử lý và tài liệu mô tả dữ liệu                   |
| `data/README.md`           | Nguồn, ngày tải, giấy phép, phiên bản/checksum và hướng dẫn lấy dữ liệu   |
| `data/data_dictionary.csv` | Tên cột, kiểu dữ liệu, đơn vị, ý nghĩa, vai trò và thời điểm có thông tin |
| `src/data.py`              | Tải và kiểm tra dữ liệu                                                   |
| `src/features.py`          | Tạo và biến đổi đặc trưng                                                 |
| `src/train.py`             | Huấn luyện và lưu mô hình                                                 |
| `src/evaluate.py`          | Đánh giá mô hình và xuất kết quả                                          |
| `src/predict.py`           | Chạy suy luận trên dữ liệu mới                                            |
| `app/backend/`             | API phục vụ dự đoán                                                       |
| `app/frontend/`            | Giao diện người dùng                                                      |
| `configs/`                 | Cấu hình chia tập, seed, mô hình và thí nghiệm                            |
| `models/`                  | Pipeline và mô hình đã huấn luyện                                         |
| `notebooks/`               | Phân tích khám phá và thử nghiệm có kiểm soát                             |
| `reports/`                 | Báo cáo và hình ảnh kết quả                                               |
| `slides/`                  | Tài liệu trình bày                                                        |
| `tests/`                   | Kiểm thử mã nguồn và pipeline                                             |
| `docs/`                    | Tài liệu dự án, quyết định kỹ thuật và tiến độ hàng tuần                  |

## Cài đặt

Yêu cầu Python 3.10 trở lên. Tạo môi trường ảo và cài đặt các thư viện:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Quy trình làm việc

1. Đặt dữ liệu gốc vào `data/raw/`.
2. Cập nhật `data/data_dictionary.csv` và `data/README.md`.
3. Xử lý dữ liệu và tạo đặc trưng bằng các module trong `src/`.
4. Huấn luyện, đánh giá và lưu pipeline vào `models/`.
5. Lưu bảng kết quả vào `reports/` và hình ảnh vào `reports/figures/`.
6. Chạy kiểm thử trước khi tích hợp API hoặc giao diện.

## Trạng thái

Dự án đang ở giai đoạn khởi tạo cấu trúc. Các module trong `src/`, backend,
frontend và bộ kiểm thử sẽ được triển khai trong các bước tiếp theo.

## Ghi chú dữ liệu

Không đưa dữ liệu khách hàng có thông tin nhận diện cá nhân hoặc dữ liệu mật
vào repository. Dữ liệu lớn và các tệp mô hình sinh ra nên được quản lý ngoài
Git hoặc bằng cơ chế lưu trữ phù hợp.
