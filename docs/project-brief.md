# PROJECT 15 — DỰ ĐOÁN KHÁCH HÀNG VIỄN THÔNG RỜI MẠNG

## 1. Bối cảnh và mục tiêu

Nhà mạng cần nhận diện những khách hàng có nguy cơ ngừng sử dụng dịch vụ để ưu tiên khảo sát chất lượng và hỗ trợ. Khi nguồn lực chăm sóc có hạn, một danh sách được xếp hạng theo nguy cơ có thể giúp nhân viên tổ chức công việc tốt hơn.

Dự án xây dựng mô hình Logistic Regression để ước tính xác suất rời mạng, đồng thời tích hợp mô hình vào ứng dụng web dành cho đội chăm sóc khách hàng. Hệ thống hỗ trợ quyết định; nhân viên vẫn chịu trách nhiệm lựa chọn hành động phù hợp.

## 2. Câu hỏi và đặc tả bài toán

Câu hỏi nghiên cứu: thông tin sử dụng dịch vụ trong chín tháng đầu có giúp Logistic Regression dự báo khách hàng rời mạng trong ba tháng tiếp theo không?

| Thành phần        | Định nghĩa                                                    |
| ----------------- | ------------------------------------------------------------- |
| Loại bài toán     | Phân loại nhị phân                                            |
| Đơn vị quan sát   | Một thuê bao được tổng hợp theo giai đoạn                     |
| Thời điểm dự đoán | Cuối giai đoạn quan sát chín tháng, theo mô tả của đề         |
| Đầu vào           | Các đặc trưng được xác minh là có sẵn trước giai đoạn kết quả |
| Nhãn              | Trạng thái churn theo định nghĩa của dataset                  |
| Đầu ra            | Xác suất churn và nhóm ưu tiên chăm sóc theo ngưỡng           |
| Người dùng        | Nhân viên hoặc đội chăm sóc khách hàng                        |

Nhóm sẽ kiểm tra định nghĩa churn, mã nhãn và thời điểm có sẵn của từng biến trước khi chốt danh sách đầu vào. Không sử dụng nhãn, mã định danh hoặc thông tin phát sinh trong giai đoạn kết quả làm đặc trưng. Mô tả chín tháng/ba tháng không đồng nghĩa dữ liệu có bản ghi riêng cho từng tháng.

## 3. Dữ liệu và phạm vi sử dụng

Dữ liệu được đề bài chỉ định là Iranian Churn Dataset trên UCI. Quy mô 3.150 khách hàng và 13 đặc trưng là thông tin ghi trong bản giao đề; nhóm chưa coi đó là kết quả kiểm tra tệp thực tế. Số cột, vai trò từng cột, giấy phép, nguồn, ngày tải và checksum sẽ được đối chiếu và ghi trong `data/README.md`, `data/data_dictionary.csv`.

Ứng dụng dùng dữ liệu công khai phục vụ học tập và dữ liệu demo an toàn. Khách hàng được biểu diễn bằng mã giả; không lưu số điện thoại. Nhóm không tự thu thập dữ liệu khách hàng thực tế trong phạm vi cốt lõi.

## 4. Phương pháp và đánh giá dự kiến

Nhóm xây dựng baseline theo tỷ lệ churn của tập train, Logistic Regression không class_weight và mô hình logistic có class_weight để so sánh. Chuẩn hóa và các bước tiền xử lý được đặt trong pipeline, chỉ học trên phần train của mỗi lần chia/fold.

Đánh giá sử dụng PR-AUC, ROC-AUC, precision, recall, F1 và calibration. Bốn thí nghiệm gồm: so sánh baseline/logistic; đánh giá chất lượng xác suất; so sánh ba ngưỡng gắn với năng lực chăm sóc; phân tích hệ số và lỗi theo thời gian sử dụng/mức phí. Chi tiết nằm trong `docs/baseline-plan.md`.

Validation/CV dùng để chọn cấu hình và ngưỡng. Test được giữ độc lập đến khi chốt quy trình. Nhóm không cam kết một mức accuracy tùy ý khi chưa có thí nghiệm.

## 5. Phạm vi ứng dụng web

Ứng dụng có ít nhất ba màn hình: giới thiệu/phạm vi; nhập thông tin hoặc tải CSV để dự đoán; dashboard đánh giá và model card. Luồng chính là kiểm tra dữ liệu đầu vào, gọi API `POST /api/churn-score`, hiển thị xác suất và danh sách ưu tiên.

Hệ thống phải báo rõ dữ liệu thiếu, sai kiểu hoặc ngoài miền; không âm thầm thay giá trị. Huấn luyện thực hiện offline, API chỉ nạp pipeline đã lưu. React + TypeScript và Python + FastAPI là phương án nhóm đề xuất, không phải yêu cầu bắt buộc của giảng viên. Đăng nhập, quản lý gói cước, thanh toán và gửi ưu đãi tự động nằm ngoài phạm vi cốt lõi.

## 6. Tiêu chí hoàn thành và giới hạn

Sản phẩm đạt yêu cầu khi pipeline tái lập được trên máy khác, có baseline và phép so sánh công bằng, bảo vệ test, hoàn thành bốn thí nghiệm và có luồng web chạy được. Nếu mô hình không vượt baseline, nhóm báo cáo trung thực và phân tích nguyên nhân. Cả hai thành viên phải hiểu toàn bộ pipeline và có minh chứng đóng góp.

Nguy cơ churn không phải xác suất giữ được khách sau ưu đãi. Hệ số mô hình không chứng minh quan hệ nhân quả. Hiệu quả trên dataset không bảo đảm hiệu quả ở nhà mạng khác. Đầu ra chỉ hỗ trợ ưu tiên liên hệ phù hợp, không dùng để quấy rối hoặc áp dụng giá khác biệt.

## 7. Trạng thái và nguồn

Đây là thiết kế tuần 1, chưa có kết quả huấn luyện hoặc xác nhận đã kiểm tra dữ liệu. Các việc cần chốt: định nghĩa/mã nhãn, ý nghĩa và thời điểm các biến, trùng lặp/ID, giấy phép và cách chia dữ liệu.

Nguồn yêu cầu: `Project_15_du_doan_khach_hang_roi_mang.docx`, các mục 1–6, PGS.TS. Nguyễn Văn Hậu, lớp 12523W.1. Nguồn dữ liệu cần đối chiếu: https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset .
