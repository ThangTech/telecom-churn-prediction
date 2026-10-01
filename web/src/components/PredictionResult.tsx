import { CAPACITY_LABELS } from '../config/model';
import type { ChurnScoreResponse, PriorityGroup } from '../types/churn';

const PRIORITY_LABELS: Record<PriorityGroup, string> = {
  HIGH: 'Ưu tiên cao',
  MEDIUM: 'Ưu tiên trung bình',
  EXTENDED: 'Theo dõi mở rộng',
  NOT_PRIORITIZED: 'Chưa thuộc nhóm ưu tiên',
};

export function PredictionResult({ result }: { result: ChurnScoreResponse }) {
  const percent = result.churn_probability * 100;
  return (
    <section className="result-card" aria-live="polite" aria-label="Kết quả dự đoán">
      {result.source === 'mock' && (
        <div className="mock-banner" role="status">
          DỮ LIỆU MÔ PHỎNG · Backend chưa được kết nối. Đây không phải kết quả từ mô hình thật.
        </div>
      )}
      <div className="result-heading">
        <div>
          <span className="eyebrow">Xác suất rời mạng ước lượng</span>
          <strong className="probability">{percent.toFixed(1)}%</strong>
        </div>
        <div className={`prediction-badge ${result.predicted_churn ? 'positive' : 'negative'}`}>
          {result.predicted_churn ? 'Vượt ngưỡng liên hệ' : 'Chưa vượt ngưỡng liên hệ'}
        </div>
      </div>
      <div className="probability-track" aria-label={`Xác suất ${percent.toFixed(1)} phần trăm`}>
        <span style={{ width: `${percent}%` }} />
        <i style={{ left: `${Math.min(result.threshold * 100, 98)}%` }} title={`Ngưỡng ${(result.threshold * 100).toFixed(2)}%`} />
      </div>
      <div className="result-grid">
        <div><span>Nhóm ưu tiên chăm sóc</span><strong>{PRIORITY_LABELS[result.priority_group]}</strong></div>
        <div><span>Ngưỡng đang áp dụng</span><strong>{result.threshold.toFixed(6)}</strong></div>
        <div><span>Chế độ công suất</span><strong>{CAPACITY_LABELS[result.capacity_mode]}</strong></div>
      </div>
      <p className="callout warning">
        Xác suất là ước lượng hỗ trợ sắp xếp ưu tiên, không phải kết luận chắc chắn. Nhân viên cần xem xét bối cảnh và không dùng điểm số cho hành động mang tính trừng phạt.
      </p>
    </section>
  );
}
