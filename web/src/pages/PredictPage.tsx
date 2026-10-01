import { type FormEvent, useState } from 'react';
import { CAPACITY_LABELS, CAPACITY_THRESHOLDS, FEATURE_DEFINITIONS, PRIMARY_CAPACITY_MODE } from '../config/model';
import { FeatureField } from '../components/FeatureField';
import { PredictionResult } from '../components/PredictionResult';
import { createEmptyFormValues, toChurnFeatures, validateFeature, validateForm, type FormErrors } from '../lib/validation';
import { ChurnApiError, scoreChurn } from '../services/churnApi';
import type { CapacityMode, ChurnScoreResponse, FeatureName } from '../types/churn';

const GROUPS = [
  { id: 'usage', title: 'Hành vi sử dụng', note: 'Các tổng hợp cuộc gọi và tin nhắn trong kỳ quan sát.' },
  { id: 'account', title: 'Thuê bao & tài khoản', note: 'Thông tin gói cước, trạng thái và tương tác dịch vụ.' },
  { id: 'profile', title: 'Hồ sơ tổng hợp', note: 'Thông tin nhân khẩu và giá trị khách hàng không định danh.' },
] as const;

export function PredictPage() {
  const [values, setValues] = useState(createEmptyFormValues);
  const [errors, setErrors] = useState<FormErrors>({});
  const [capacityMode, setCapacityMode] = useState<CapacityMode>(PRIMARY_CAPACITY_MODE);
  const [result, setResult] = useState<ChurnScoreResponse | null>(null);
  const [apiError, setApiError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const updateValue = (name: FeatureName, value: string) => {
    setValues((current) => ({ ...current, [name]: value }));
    if (errors[name]) setErrors((current) => ({ ...current, [name]: validateFeature(name, value) }));
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (submitting) return;
    const nextErrors = validateForm(values);
    setErrors(nextErrors);
    setApiError('');
    setResult(null);
    if (Object.keys(nextErrors).length > 0) return;

    setSubmitting(true);
    try {
      const response = await scoreChurn({ features: toChurnFeatures(values), capacity_mode: capacityMode });
      setResult(response);
    } catch (error) {
      setApiError(error instanceof ChurnApiError ? error.message : 'Đã xảy ra lỗi không xác định. Vui lòng thử lại.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page-width page-stack">
      <header className="page-header split-header">
        <div><span className="eyebrow">CHẤM ĐIỂM KHÁCH HÀNG</span><h1>Dự đoán nguy cơ rời mạng</h1><p>Nhập đủ 13 thuộc tính. Dữ liệu sai sẽ được báo rõ, không tự động thay thế.</p></div>
        <div className="privacy-note"><span aria-hidden="true">◎</span><div><strong>Không nhập dữ liệu định danh</strong><small>Không thu thập số điện thoại thật, họ tên hoặc địa chỉ.</small></div></div>
      </header>

      <form className="prediction-form" onSubmit={handleSubmit} noValidate>
        {GROUPS.map((group, groupIndex) => (
          <section className="form-section" key={group.id}>
            <div className="form-section-heading"><span>{String(groupIndex + 1).padStart(2, '0')}</span><div><h2>{group.title}</h2><p>{group.note}</p></div></div>
            <div className="form-grid">
              {FEATURE_DEFINITIONS.filter((feature) => feature.group === group.id).map((feature) => (
                <FeatureField
                  key={feature.name}
                  feature={feature}
                  value={values[feature.name]}
                  error={errors[feature.name]}
                  onChange={(value) => updateValue(feature.name, value)}
                  onBlur={() => setErrors((current) => ({ ...current, [feature.name]: validateFeature(feature.name, values[feature.name]) }))}
                />
              ))}
            </div>
          </section>
        ))}

        <section className="capacity-panel">
          <div><span className="eyebrow">NGƯỠNG ĐÃ ĐÓNG BĂNG</span><h2>Chọn công suất chăm sóc</h2><p>Công suất cao cho phép liên hệ nhiều khách hàng hơn nên dùng ngưỡng thấp hơn. Đây không phải mức nguy cơ.</p></div>
          <div className="capacity-options">
            {(Object.keys(CAPACITY_THRESHOLDS) as CapacityMode[]).map((mode) => (
              <label key={mode} className={capacityMode === mode ? 'selected' : ''}>
                <input type="radio" name="capacity" value={mode} checked={capacityMode === mode} onChange={() => setCapacityMode(mode)} />
                <span><strong>{CAPACITY_LABELS[mode].split(' · ')[0]}</strong><small>Ngưỡng {CAPACITY_THRESHOLDS[mode].toFixed(6)}</small></span>
              </label>
            ))}
          </div>
          <p className="capacity-caveat">Tỷ lệ 10% / 20% / 30% là độ bao phủ mục tiêu xấp xỉ trên validation; sau khi refit, dữ liệu mới không được đảm bảo có đúng tỷ lệ này.</p>
        </section>

        {Object.keys(errors).length > 0 && <div className="form-alert" role="alert">Có {Object.keys(errors).length} trường cần kiểm tra trước khi gửi.</div>}
        {apiError && <div className="form-alert api" role="alert"><strong>Không thể dự đoán.</strong> {apiError}</div>}
        <div className="submit-row">
          <span>Target Churn và row_id không được gửi tới mô hình.</span>
          <button className="button primary submit-button" type="submit" disabled={submitting}>
            {submitting ? <><i className="spinner" /> Đang dự đoán…</> : <>Dự đoán nguy cơ rời mạng <span aria-hidden="true">→</span></>}
          </button>
        </div>
      </form>
      {result && <PredictionResult result={result} />}
    </div>
  );
}
