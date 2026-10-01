import { CAPACITY_THRESHOLDS, PUBLISHED_METRICS } from '../config/model';

const format = (value: number) => value.toFixed(6);

export function ModelCardPage() {
  return (
    <div className="page-width page-stack model-card-page">
      <header className="page-header model-hero">
        <div><span className="eyebrow">MODEL CARD · WEEK 4 FROZEN</span><h1>Logistic Regression</h1><p>Mô hình phân loại xác suất hỗ trợ xếp hạng khách hàng viễn thông có khả năng rời mạng.</p></div>
        <div className="final-badge"><span>Trạng thái</span><strong>FINAL</strong><small>Test không dùng để tuning</small></div>
      </header>

      <section className="model-overview-grid">
        <article><span>Dataset</span><strong>Iranian Churn</strong><small>3.150 bản ghi · UCI dataset 563</small></article>
        <article><span>Candidate</span><strong>C = 10</strong><small>class_weight = None</small></article>
        <article><span>Quan sát</span><strong>9 tháng</strong><small>Dự đoán churn đến cuối tháng 12</small></article>
        <article><span>Primary threshold</span><strong>0.343183</strong><small>Công suất trung bình</small></article>
      </section>

      <section className="panel metrics-section">
        <div className="section-heading"><span className="eyebrow">HIỆU NĂNG ĐÃ CÔNG BỐ</span><h2>Validation và test được tách biệt</h2><p>Test được đánh giá đúng một lần sau khi mọi quyết định đã đóng băng.</p></div>
        <div className="metric-comparison">
          <div className="metric-column"><h3>Validation <small>candidate fit trên train</small></h3>
            <dl><div><dt>PR-AUC</dt><dd>{format(PUBLISHED_METRICS.validation.prAuc)}</dd></div><div><dt>Average Precision</dt><dd>{format(PUBLISHED_METRICS.validation.averagePrecision)}</dd></div><div><dt>ROC-AUC</dt><dd>{format(PUBLISHED_METRICS.validation.rocAuc)}</dd></div><div><dt>Brier ↓</dt><dd>{format(PUBLISHED_METRICS.validation.brier)}</dd></div></dl>
          </div>
          <div className="metric-column test"><h3>Final test <small>fit trên train + validation</small></h3>
            <dl><div><dt>PR-AUC</dt><dd>{format(PUBLISHED_METRICS.test.prAuc)}</dd></div><div><dt>Average Precision</dt><dd>{format(PUBLISHED_METRICS.test.averagePrecision)}</dd></div><div><dt>ROC-AUC</dt><dd>{format(PUBLISHED_METRICS.test.rocAuc)}</dd></div><div><dt>Brier ↓</dt><dd>{format(PUBLISHED_METRICS.test.brier)}</dd></div><div><dt>Precision</dt><dd>{format(PUBLISHED_METRICS.test.precision)}</dd></div><div><dt>Recall</dt><dd>{format(PUBLISHED_METRICS.test.recall)}</dd></div><div><dt>F1</dt><dd>{format(PUBLISHED_METRICS.test.f1)}</dd></div></dl>
          </div>
        </div>
      </section>

      <section className="threshold-section">
        <div className="section-heading"><span className="eyebrow">CÔNG SUẤT CHĂM SÓC</span><h2>Ba ngưỡng đã đóng băng</h2><p>Ngưỡng được chọn trên validation trước khi mở test.</p></div>
        <div className="threshold-cards">
          <article><span>LOW · ~10% validation</span><strong>{CAPACITY_THRESHOLDS.LOW.toFixed(6)}</strong><p>Công suất thấp → ngưỡng cao hơn.</p></article>
          <article className="primary-threshold"><span>MEDIUM · ~20% validation</span><strong>{CAPACITY_THRESHOLDS.MEDIUM.toFixed(6)}</strong><p>Ngưỡng chính của báo cáo.</p></article>
          <article><span>HIGH · ~30% validation</span><strong>{CAPACITY_THRESHOLDS.HIGH.toFixed(6)}</strong><p>Công suất cao → ngưỡng thấp hơn.</p></article>
        </div>
        <p className="callout">Sau final refit trên train + validation, thang xác suất có thể dịch chuyển. Vì vậy độ bao phủ trên dữ liệu mới chỉ là xấp xỉ, không được đảm bảo chính xác 10% / 20% / 30%.</p>
      </section>

      <div className="model-details-grid">
        <section className="panel"><span className="eyebrow">MỤC ĐÍCH SỬ DỤNG</span><h2>Hỗ trợ, không tự động quyết định</h2><ul className="check-list"><li>Ưu tiên khách hàng có thể cần được hỗ trợ.</li><li>Dùng trong phạm vi nguồn lực chăm sóc đã xác định.</li><li>Luôn có nhân viên xem xét trước khi hành động.</li></ul></section>
        <section className="panel danger-panel"><span className="eyebrow">KHÔNG DÙNG CHO</span><h2>Giới hạn quyết định</h2><ul className="cross-list"><li>Định giá phân biệt hoặc từ chối dịch vụ.</li><li>Kết luận nguyên nhân khách hàng rời mạng.</li><li>Suy ra khả năng phản hồi ưu đãi chăm sóc.</li><li>Áp dụng cho quần thể khác khi chưa đánh giá lại.</li></ul></section>
      </div>

      <section className="panel limitations">
        <div><span className="eyebrow">GIỚI HẠN & QUẢN TRỊ</span><h2>Những điều cần biết trước khi sử dụng</h2></div>
        <div className="limitation-grid">
          <article><strong>Phạm vi dữ liệu</strong><p>Chỉ 3.150 bản ghi từ một bộ dữ liệu/quần thể. Dữ liệu ngoài miền cần được đánh giá mới.</p></article>
          <article><strong>Customer Value</strong><p>UCI gọi đây là “calculated value of customer”, nhưng công thức và thành phần chính xác chưa công bố.</p></article>
          <article><strong>Không phải quan hệ nhân quả</strong><p>Hệ số và xác suất thể hiện liên hệ thống kê, không chứng minh nguyên nhân churn.</p></article>
          <article><strong>Drift & fairness</strong><p>Cần theo dõi drift, calibration và tác động khác biệt; hiện không có tuyên bố công bằng cho các nhóm.</p></article>
        </div>
      </section>
    </div>
  );
}
