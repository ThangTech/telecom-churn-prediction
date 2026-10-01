import { Link } from 'react-router-dom';

export function HomePage() {
  return (
    <>
      <section className="hero page-width">
        <div className="hero-copy">
          <span className="eyebrow">PROJECT 15 · MACHINE LEARNING</span>
          <h1>Nhìn thấy tín hiệu rời mạng, <em>trước khi quá muộn.</em></h1>
          <p>
            Hệ thống ước lượng xác suất khách hàng viễn thông rời mạng, giúp đội chăm sóc ưu tiên hoạt động hỗ trợ một cách minh bạch và có kiểm soát.
          </p>
          <div className="hero-actions">
            <Link className="button primary" to="/predict">Bắt đầu dự đoán <span aria-hidden="true">→</span></Link>
            <Link className="button secondary" to="/model-card">Xem Model Card</Link>
          </div>
          <div className="hero-facts" aria-label="Thông tin mô hình">
            <div><strong>13</strong><span>thuộc tính đầu vào</span></div>
            <div><strong>9 + 3</strong><span>tháng quan sát + dự đoán</span></div>
            <div><strong>0.343183</strong><span>ngưỡng chính</span></div>
          </div>
        </div>
        <div className="hero-visual" aria-label="Minh họa quy trình chấm điểm">
          <div className="orb orb-one" />
          <div className="orb orb-two" />
          <div className="signal-card">
            <span className="signal-label">Tín hiệu nguy cơ</span>
            <div className="signal-value">68.4<small>%</small></div>
            <div className="sparkline" aria-hidden="true">
              {[25, 30, 26, 46, 40, 57, 52, 68].map((height, index) => <i key={index} style={{ height: `${height}%` }} />)}
            </div>
            <span className="signal-status"><i /> Cần nhân viên xem xét</span>
          </div>
          <div className="floating-card top"><b>Logistic Regression</b><span>Mô hình xác suất dễ diễn giải</span></div>
          <div className="floating-card bottom"><b>Iranian Churn</b><span>3.150 quan sát</span></div>
        </div>
      </section>

      <section className="how-it-works page-width">
        <div className="section-heading"><span className="eyebrow">QUY TRÌNH SỬ DỤNG</span><h2>Ba bước từ dữ liệu đến hành động</h2></div>
        <div className="steps">
          <article><span>01</span><h3>Nhập thông tin</h3><p>Cung cấp 13 thuộc tính tổng hợp trong 9 tháng đầu. Không cần số điện thoại hay thông tin định danh.</p></article>
          <article><span>02</span><h3>Nhận xác suất</h3><p>Backend áp dụng pipeline Logistic Regression đã đóng băng để trả về xác suất churn.</p></article>
          <article><span>03</span><h3>Ưu tiên hỗ trợ</h3><p>So sánh với ngưỡng công suất đã chọn, sau đó để nhân viên quyết định cách hỗ trợ phù hợp.</p></article>
        </div>
      </section>

      <section className="observation-strip">
        <div className="page-width timeline-copy">
          <div><span className="eyebrow">CỬA SỔ THỜI GIAN</span><h2>Quan sát 9 tháng.<br />Dự đoán 3 tháng tiếp theo.</h2></div>
          <div className="timeline" aria-label="Dòng thời gian dự đoán">
            <div className="timeline-segment observe"><span>Tháng 1–9</span><strong>Tổng hợp thuộc tính</strong></div>
            <div className="timeline-segment gap"><span>Tháng 10–12</span><strong>Khoảng dự đoán churn</strong></div>
          </div>
        </div>
      </section>
    </>
  );
}
