# Week 3 — Phan Duy Sơn

## Công việc thực hiện

- Audit feature eligibility và đối chiếu data dictionary/config Week 3.
- Review `Status` và `Customer Value` theo prediction point.
- Review preprocessing của Logistic Regression pipeline.
- Phân tích class_weight, C, candidate, validation confusion matrix và calibration.
- Review 13 tests hiện có và bổ sung bốn tests còn thiếu.
- Không đánh giá test, không chọn threshold cuối, không chạy Week 4.

## Kết quả

- Feature set giữ nguyên 11 biến.
- `Status`: UNRESOLVED — SOURCE VERIFICATION REQUIRED.
- `Customer Value`: UNRESOLVED — SOURCE VERIFICATION REQUIRED.
- Candidate provisional: class_weight=None, C=10, chọn bằng mean train-CV AP 0,73897 ± 0,06574.
- Validation: AP 0,76393; ROC-AUC 0,93345; Brier 0,07068; precision 0,88462; recall 0,46465; F1 0,60927.
- Confusion matrix validation: TN=525, FP=6, FN=53, TP=46.
- Không rerun experiments vì feature set không đổi.
- Feature set được ghi rõ là provisional, không phải final.

## Review phần Thắng

- CV chỉ chạy trên train với grouped folds và refit toàn bộ pipeline từng fold.
- Validation không tham gia chọn C/class_weight; candidate chọn theo mean CV AP.
- Pipeline xử lý numeric/categorical hợp lý và hỗ trợ unseen category.
- Balanced tăng recall nhưng giảm precision và calibration; không tốt hơn tuyệt đối.
- C=10 đứng đầu mean AP nhưng chênh lệch nhỏ hơn nhiều so với fold variability.
- Test set được ghi `test_evaluated=false`; không có test metric trong artifact được review.

## Đóng góp trực tiếp của Sơn

- Feature/metadata audit cho `Status` và `Customer Value`.
- Diễn giải class_weight, C, validation, calibration và confusion matrix.
- Test eligibility chạy độc lập trên branch Sơn và bốn integration tests có conditional skip rõ ràng.
- Xác minh checksum CRLF/LF bằng bytes của file hiện tại và cập nhật provenance note.
- Viết báo cáo phân tích và weekly report; không chạy lại model của Thắng.

## File tạo

- `reports/week3-son-analysis.md`
- `docs/weekly/week-03-son.md`
- `tests/test_son_week3.py`

## File cập nhật

- `data/README.md`
- `docs/decisions.md`
- `reports/data-quality.md` (regenerated)
- `scripts/validate_week2.py`

Không cập nhật `src/features.py` hoặc `data/data_dictionary.csv` vì không có bằng chứng mới để thay đổi feature decision.

## Test trên branch Sơn

- Total: 13.
- Passed: 9 unit tests.
- Failed: 0.
- Skipped: 4 integration tests phụ thuộc module/artifact Week 3 của Thắng chưa có trên branch Sơn.
- Mỗi skip có message rõ; bốn integration tests đã pass trên snapshot tạm có code Thắng.
- Test set không được evaluate.

## Dataset provenance/checksum

Checkout CRLF có MD5 `e5362c3e5787dadd4e21eb606509bc03` và SHA256 `90d5fb6bd1630cd4de4b4d28fcf8b4cb92a8f6ab7484605b0799d47386f7dbe1`. Chuẩn hóa line endings sang LF cho cùng nội dung tạo MD5 `07311e7080c0fb5b0ce94f5977abc4d5`, khớp checksum tham chiếu. Row parsing, `row_id` và split không đổi nên không tạo split mới. Source URL/license/citation vẫn pending.

## Vấn đề và quyết định

- Giữ `Status` và `Customer Value` ngoài model.
- Giữ candidate ở trạng thái provisional.
- Không đổi preprocessing hoặc threshold.
- Branch `Son` chưa tích hợp commit Week 3 của Thắng; review dùng snapshot read-only của `origin/Thang`.

## Giờ ước lượng

Chưa ghi nhận; Sơn bổ sung thời gian thực tế của cá nhân khi nộp báo cáo.

## Commit/PR

Chưa tạo theo yêu cầu. Không commit và không push.

## Trạng thái

COMPLETE cho phần cá nhân Week 3 của Sơn. Group integration có thể thực hiện sau; candidate và feature set vẫn provisional cho đến khi nhóm chấp nhận rõ các blocker metadata.
