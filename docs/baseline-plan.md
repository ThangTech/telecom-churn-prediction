# Kế hoạch baseline và đánh giá — Project 15

Trạng thái: kế hoạch tuần 1, chưa chạy thí nghiệm. Yêu cầu lấy từ DOCX Project 15; các lựa chọn triển khai dưới đây là đề xuất để nhóm review và chốt trước khi đánh giá test.

## 1. Mục đích

Kiểm tra mô hình có tạo giá trị hơn mốc đơn giản và việc thay đổi trọng số lớp có cải thiện khả năng nhận diện khách hàng churn hay không. Không chọn mô hình chỉ bằng accuracy cao nhất.

## 2. Các phương án so sánh

| Mã | Phương án | Vai trò |
|---|---|---|
| B0 | Mỗi khách nhận cùng xác suất bằng tỷ lệ churn trong train | Đề xuất cụ thể hóa baseline theo tỷ lệ churn |
| B1 | Tiền xử lý + StandardScaler cho biến số + LogisticRegression(class_weight=None) | Baseline mô hình theo đề |
| M1 | Cùng tiền xử lý + LogisticRegression(class_weight='balanced') | Đề xuất cấu hình để so sánh class_weight |

B0 tính p = số mẫu churn / tổng số mẫu của phần train tương ứng. Đây là baseline xác suất hằng, không giả vờ xếp hạng được khách hàng. Nếu báo metric phân loại, phải ghi ngưỡng áp dụng. Không dùng tỷ lệ test để tạo dự đoán baseline.

B1 và M1 dùng cùng đặc trưng, split, cách đánh giá và ngân sách tìm cấu hình. Trước hết so sánh trực tiếp chỉ thay class_weight để thấy tác động; nếu tuning thêm thì ghi thành thí nghiệm riêng. Cấu hình balanced là lựa chọn nhóm đề xuất, không phải tham số duy nhất thầy bắt buộc.

## 3. Kiểm tra dữ liệu trước mô hình

- Xác minh nhãn, mã lớp dương, ý nghĩa các cột, đơn vị và thời điểm có thông tin.
- Đối chiếu số dòng/cột thực tế, ID và các bản ghi trùng/khả năng cùng thuê bao.
- Không dùng nhãn để chọn loại ngoại lệ; không xóa hàng chỉ vì làm mô hình kém.
- Chưa chốt một cột là hợp lệ chỉ vì tên có vẻ hợp lý; ghi rõ biến chưa xác minh.
- Quy tắc xử lý missing, encoder, scaler phải phù hợp với loại biến thực tế.

## 4. Chia tập và bảo vệ test

Phương án dự kiến nếu dữ liệu không có cấu trúc thời gian/nhóm cần ưu tiên: chia stratified train/validation/test. Tỷ lệ sẽ chốt sau khi kiểm tra số mẫu và số mẫu lớp dương; không thay tỷ lệ chỉ để lấy điểm cao hơn. Nếu có cấu trúc nhóm hoặc thời gian có ý nghĩa, điều chỉnh cách chia và ghi lý do.

Bản ghi trùng hoặc cùng đối tượng đã xác định không được rơi vào các tập khác nhau. Nếu thiếu ID để xác minh, ghi giới hạn thay vì khẳng định đã tách theo khách hàng.

Quy trình:
1. Chốt quy tắc chia, seed cố định (đề xuất 42), lưu chỉ số tập và checksum dữ liệu.
2. EDA phục vụ lựa chọn tiền xử lý trên train. Không dùng phân tích test để chọn đặc trưng/cấu hình.
3. Fit imputer, encoder, scaler trên train; trong CV, fit lại trong từng fold train.
4. Dùng validation/CV để chọn cấu hình và ba ngưỡng.
5. Đóng băng đặc trưng, pipeline, cấu hình, ngưỡng và quy tắc báo cáo trước test.
6. Theo lịch DOCX, đánh giá test cuối ở tuần 4; không sửa mô hình theo lỗi test rồi báo lại như đánh giá độc lập.

Nếu phát hiện lỗi kỹ thuật buộc chạy lại, phải ghi lỗi, số lần và tác động; không che giấu. Tuần 6 tái lập cùng quy trình đã chốt, không mở vòng tuning mới.

## 5. Tiền xử lý và lưu mô hình

Tiền xử lý dự kiến theo loại dữ liệu: xử lý missing nếu có, mã hóa biến phân loại, StandardScaler cho biến số. Không scale biến chỉ vì nó được lưu dạng số: phải xem đó là số đo hay mã loại.

Kế hoạch cốt lõi chưa dùng SMOTE. Nếu bổ sung, chỉ resample trong fold train, không trước split và không trên validation/test. Lưu toàn bộ pipeline để API dùng lại đúng biến đổi, cùng danh sách/thứ tự đặc trưng và schema.

## 6. Bốn thí nghiệm bắt buộc

| Thí nghiệm | Thiết kế | Minh chứng |
|---|---|---|
| Baseline và logistic | So sánh B0, B1, M1 cùng split | Bảng metric, cấu hình và nhận xét |
| Xác suất/calibration | Reliability diagram; có thể thêm Brier score | Biểu đồ, số mẫu mỗi bin, phân tích xác suất quá cao/thấp |
| Ba ngưỡng theo năng lực | Chọn ba mức trên validation, công bố giả định công suất | Ngưỡng, số/tỷ lệ khách được chọn, precision, recall, F1, TP/FP/FN/TN |
| Hệ số và lỗi | Phân tích hệ số sau tiền xử lý và sai số theo tenure/charge đã xác minh | Bảng/hình theo nhóm, số mẫu, ví dụ lỗi, giới hạn |

Đánh giá calibration không đồng nghĩa bắt buộc hiệu chỉnh xác suất. Nếu thêm hiệu chỉnh, chỉ học trên dữ liệu phát triển phù hợp, không fit trên test. class_weight có thể thay đổi chất lượng xác suất nên phải kiểm tra chứ không mặc định tốt hơn.

Tên tenure/charge ở đây theo yêu cầu đề, chưa phải xác nhận tên cột trong tệp. Nhóm sẽ ánh xạ bằng data dictionary.

## 7. Metric và cách diễn giải

Chọn churn là lớp dương sau khi xác minh mã nhãn.

- Precision = TP/(TP+FP): trong danh sách dự đoán churn, tỷ lệ thực sự churn.
- Recall = TP/(TP+FN): tìm được bao nhiêu trong số người thực sự churn.
- F1: trung bình điều hòa precision và recall.
- ROC-AUC: đánh giá khả năng phân biệt qua nhiều ngưỡng.
- PR-AUC: đánh giá đường precision–recall, đặc biệt cần xem khi lớp churn ít.
- Calibration: so sánh xác suất dự đoán với tần suất churn thực tế.

Accuracy chỉ bổ trợ. Nhóm dự kiến dùng Average Precision (AP) làm bản tóm tắt PR curve và ghi rõ AP trong bảng; AP không hoàn toàn giống diện tích hình thang dưới đường PR. Nếu rubric yêu cầu cách tính PR-AUC cụ thể, xác nhận và ghi chính xác phương pháp.

Nếu không có dự đoán dương, báo precision không xác định hoặc ghi rõ quy ước của thư viện; không diễn giải con số thay thế như hiệu quả tốt. Khi so sánh nhiều seed/fold, làm trên dữ liệu phát triển và báo biến thiên, không chọn seed tốt nhất hay thử nhiều test split.

## 8. Ngưỡng và năng lực chăm sóc

Ngưỡng chuyển xác suất thành nhãn ưu tiên. Đề xuất ba kịch bản công suất thấp/vừa/cao; tỷ lệ hoặc số lượng cụ thể phải chốt bằng giả định minh bạch trước test. Chọn ngưỡng trên validation sao cho danh sách phù hợp kịch bản và báo đánh đổi precision/recall.

Giữ nguyên ngưỡng khi đánh giá test; số người được chọn trên test có thể khác dự kiến. Ngưỡng cố định không bảo đảm đúng N người. Chọn Top-N là chính sách khác, chỉ bổ sung nếu mô tả rõ và không thay thế thí nghiệm ba ngưỡng. Không gọi điểm cosine, xác suất churn hay ngưỡng là accuracy.

## 9. Đầu ra, trách nhiệm và việc còn mở

Lưu cấu hình, seed, phiên bản thư viện, chỉ số split, bảng validation/test tách biệt, biểu đồ và pipeline. `src/train.py` và `src/evaluate.py` tách vai trò; ứng dụng chỉ suy luận từ pipeline đã lưu.

Thắng phụ trách bản kế hoạch; thành viên còn lại review với data dictionary. Hai người cùng chốt trước huấn luyện: nhãn/feature hợp lệ, split, baseline B0, định nghĩa PR-AUC, ngân sách tuning và ba kịch bản công suất. Chưa có số liệu hay kết luận mô hình nào được tạo ở tuần 1.

Nguồn yêu cầu: `Project_15_du_doan_khach_hang_roi_mang.docx`, mục 2, 3, 5 và 6. Nguồn cần tham khảo khi triển khai: trang UCI của Iranian Churn Dataset; tài liệu Logistic Regression và metric của scikit-learn. Các tài liệu này chưa được tuyên bố là nhóm đã kiểm chứng trong bản kế hoạch.
