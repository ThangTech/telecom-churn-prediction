import { useMemo, useState } from 'react';
import { CAPACITY_THRESHOLDS, PUBLISHED_METRICS } from '../config/model';
import { DEMO_PREDICTIONS } from '../data/demoPredictions';
import type { PriorityGroup } from '../types/churn';

const PRIORITY_LABELS: Record<PriorityGroup, string> = {
  HIGH: 'Ưu tiên cao', MEDIUM: 'Ưu tiên trung bình', EXTENDED: 'Theo dõi mở rộng', NOT_PRIORITIZED: 'Chưa ưu tiên',
};

export function DashboardPage() {
  const [filter, setFilter] = useState<'ALL' | PriorityGroup>('ALL');
  const rows = useMemo(
    () => DEMO_PREDICTIONS.filter((row) => filter === 'ALL' || row.priority === filter).sort((a, b) => b.probability - a.probability),
    [filter],
  );
  const groups = (Object.keys(PRIORITY_LABELS) as PriorityGroup[]).map((priority) => ({
    priority,
    count: DEMO_PREDICTIONS.filter((row) => row.priority === priority).length,
  }));

  return (
    <div className="page-width page-stack dashboard-page">
      <header className="page-header split-header">
        <div><span className="eyebrow">TỔNG QUAN VẬN HÀNH</span><h1>Dashboard chăm sóc khách hàng</h1><p>Minh họa cách sắp xếp ưu tiên theo xác suất giảm dần.</p></div>
        <div className="demo-label"><span>DEMO</span><div><strong>Dữ liệu giả lập an toàn</strong><small>Không phải tập test và không chứa thông tin cá nhân.</small></div></div>
      </header>

      <section className="stat-grid" aria-label="Chỉ số dữ liệu demo">
        <article><span>Tổng bản ghi demo</span><strong>{DEMO_PREDICTIONS.length}</strong><small>Mã khách hàng giả</small></article>
        <article><span>Vượt ngưỡng chính</span><strong>{DEMO_PREDICTIONS.filter((row) => row.probability >= CAPACITY_THRESHOLDS.MEDIUM).length}</strong><small>Ngưỡng 0.343183</small></article>
        <article><span>Xác suất trung bình demo</span><strong>{(DEMO_PREDICTIONS.reduce((sum, row) => sum + row.probability, 0) / DEMO_PREDICTIONS.length * 100).toFixed(1)}%</strong><small>Không phải metric hiệu năng</small></article>
        <article className="accent-stat"><span>Test PR-AUC công bố</span><strong>{PUBLISHED_METRICS.test.prAuc.toFixed(3)}</strong><small>Đánh giá Week 4 đã đóng băng</small></article>
      </section>

      <div className="dashboard-grid">
        <section className="panel distribution-panel">
          <div className="panel-heading"><div><span className="eyebrow">PHÂN BỐ DEMO</span><h2>Số khách hàng theo nhóm ưu tiên</h2></div><span className="unit-pill">Đơn vị: bản ghi</span></div>
          <div className="bar-chart" role="img" aria-label="Biểu đồ số bản ghi demo theo nhóm ưu tiên">
            {groups.map((group) => (
              <div className="bar-column" key={group.priority}>
                <span>{group.count}</span>
                <div><i className={`bar-${group.priority.toLowerCase()}`} style={{ height: `${Math.max(group.count * 28, 12)}%` }} /></div>
                <small>{PRIORITY_LABELS[group.priority]}</small>
              </div>
            ))}
          </div>
          <div className="chart-legend"><span><i className="legend-high" /> Demo theo ngưỡng đóng băng</span><span>Không đại diện phân bố thực tế</span></div>
        </section>

        <aside className="panel model-summary">
          <span className="eyebrow">MÔ HÌNH ĐANG DÙNG</span><h2>Logistic Regression</h2>
          <dl><div><dt>Feature</dt><dd>13</dd></div><div><dt>Final fit</dt><dd>Train + validation</dd></div><div><dt>Ngưỡng chính</dt><dd>0.343183</dd></div><div><dt>Test count</dt><dd>1 lần</dd></div></dl>
          <p>Xác suất hỗ trợ ưu tiên liên hệ, không giải thích nguyên nhân churn và không dự đoán khả năng phản hồi chính sách chăm sóc.</p>
        </aside>
      </div>

      <section className="panel table-panel">
        <div className="panel-heading">
          <div><span className="eyebrow">DANH SÁCH ƯU TIÊN</span><h2>Kết quả dự đoán minh họa</h2></div>
          <label className="filter-control">Lọc nhóm
            <select value={filter} onChange={(event) => setFilter(event.target.value as typeof filter)}>
              <option value="ALL">Tất cả</option>
              {Object.entries(PRIORITY_LABELS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
            </select>
          </label>
        </div>
        <div className="table-scroll">
          <table>
            <thead><tr><th>Mã demo</th><th>Xác suất churn</th><th>Nhóm ưu tiên</th><th>Trạng thái</th></tr></thead>
            <tbody>{rows.map((row) => (
              <tr key={row.customerId}>
                <td><strong>{row.customerId}</strong></td>
                <td><div className="table-probability"><span><i style={{ width: `${row.probability * 100}%` }} /></span><strong>{(row.probability * 100).toFixed(1)}%</strong></div></td>
                <td><span className={`priority-tag priority-${row.priority.toLowerCase()}`}>{PRIORITY_LABELS[row.priority]}</span></td>
                <td>{row.status}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
