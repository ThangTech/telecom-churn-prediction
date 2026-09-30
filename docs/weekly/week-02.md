# Week 2 - Phan Duy Sơn

## Công việc

- Chuẩn hóa loader, schema validation và data dictionary.
- Tạo stable `row_id`, split tái lập và assertions chống overlap.
- Giữ nguyên duplicate content nhưng ngăn nội dung giống hệt đi qua nhiều split.
- Thực hiện EDA canonical chỉ trên train.
- Lập leakage audit theo thời điểm feature có sẵn.
- Tạo feature eligibility và automated tests chuẩn bị cho Logistic Regression.

## Dataset validation

- CSV đọc được: 3.150 dòng, 14 cột raw.
- `row_id` được thêm ngay khi load, trước cleaning/split.
- Dictionary dùng chuẩn `column_name` và `data_type`.
- Dictionary/schema sai sẽ raise error; không còn silent fallback.
- Target duy nhất phải là `Churn`.

## Data quality

- Missing: 0.
- Target là nhị phân 0/1.
- Không tự xóa record hoặc outlier.
- Chi tiết được tạo lại bằng `scripts/validate_week2.py` trong `reports/data-quality.md`.

## Split

- Khoảng 60/20/20 bằng `StratifiedGroupKFold` năm fold.
- Ba fold train, một validation, một test.
- Stratify theo `Churn`, `random_state=42`.
- Pairwise `row_id` disjoint và union bao phủ toàn bộ nguồn.
- Duplicate content được giữ trong cùng một partition.
- Cùng seed tạo cùng assignment.

## EDA

- Implementation canonical: `scripts/eda_train.py`.
- Chỉ train được dùng cho target distribution, missing, duplicate, descriptive statistics, feature distributions và correlation heatmap.
- Validation/test không được dùng để chọn feature, preprocessing, threshold hoặc class weight.
- Mỗi biểu đồ có Purpose, Finding, Limitation và Allowed conclusion trong `reports/eda_results_week2.md`.

## Duplicate finding

- Raw: 3.150 record.
- Unique row contents: 2.850.
- Excess duplicate rows: 300.
- Duplicate groups: 165.
- Không có bằng chứng repository cho phép gọi đây là lỗi thu thập, nên giữ mặc định và ghi `Needs verification`.

## Leakage audit

Leakage được đánh giá theo định nghĩa, lineage và availability trước prediction point; không dùng ngưỡng correlation/churn rate. Chi tiết: `reports/leakage-audit.md`.

## Status

`Needs verification`. Repository không có định nghĩa hoặc thời điểm cập nhật đáng tin cậy. Biến bị loại khỏi feature set mặc định.

## Customer Value

`Needs verification`. Repository không có công thức hoặc aggregation window đáng tin cậy. Biến bị loại khỏi feature set mặc định.

## Checksum/provenance

- Repository CSV MD5: `e5362c3e5787dadd4e21eb606509bc03`.
- Source/reference checksum được cung cấp: `07311e7080c0fb5b0ce94f5977abc4d5`.
- Hai artifact không khớp. Không có ZIP hay conversion script trong repository để giải thích. Provenance còn pending.

## Problems found

- Dictionary key mismatch và silent fallback.
- Overlap check dùng index sau reset.
- Cleaning tự xóa 300 record.
- Leakage conclusion dựa trên correlation/churn rate.
- Ba implementation EDA mâu thuẫn.
- Báo cáo cũ mâu thuẫn về duplicate, môi trường và feature decision.

## Fixes

- Validation fail-fast, stable `row_id`, grouped stratified split và automated assertions.
- Cleaning không xóa dòng.
- Một EDA canonical; entry point cũ chỉ delegate.
- Pending features được chặn tại `src/features.py`.
- Báo cáo canonical được tái tạo bằng code.

## Decisions for Week 3

- Dùng 11 feature trong `CONFIRMED_MODEL_FEATURES`.
- `Churn` là target; `row_id` technical.
- Không đưa `Status`/`Customer Value` vào model nếu chưa có bằng chứng.
- Fit `StandardScaler` và Logistic Regression trong Pipeline trên train/train fold.
- So sánh `class_weight=None` và `class_weight="balanced"` bằng validation; test chỉ dùng báo cáo cuối.

## Remaining verification

- Nguồn/license/citation chính thức và checksum provenance.
- Định nghĩa/availability của `Status` và `Customer Value`.
- Bản chất nghiệp vụ của duplicate content.

## Output files

- `reports/data-quality.md`
- `reports/eda_results_week2.md`
- `reports/leakage-audit.md`
- `reports/figures/*.png`
- `tests/test_week2.py`
