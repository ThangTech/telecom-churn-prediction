import type { CapacityMode, FeatureDefinition } from '../types/churn';

export const CAPACITY_THRESHOLDS: Readonly<Record<CapacityMode, number>> = {
  LOW: 0.47683299575833915,
  MEDIUM: 0.3431830803885034,
  HIGH: 0.16505680661293284,
};

export const PRIMARY_CAPACITY_MODE: CapacityMode = 'MEDIUM';

export const CAPACITY_LABELS: Readonly<Record<CapacityMode, string>> = {
  LOW: 'Công suất chăm sóc thấp · khoảng 10% trên validation',
  MEDIUM: 'Công suất chăm sóc trung bình · khoảng 20% trên validation',
  HIGH: 'Công suất chăm sóc cao · khoảng 30% trên validation',
};

export const FEATURE_DEFINITIONS: readonly FeatureDefinition[] = [
  { name: 'Call  Failure', label: 'Số lần cuộc gọi thất bại', description: 'Tổng số lần gọi không thành công trong kỳ quan sát.', unit: 'lần', group: 'usage', kind: 'integer', min: 0 },
  { name: 'Complains', label: 'Có khiếu nại', description: 'Khách hàng có phát sinh khiếu nại hay không.', unit: 'nhị phân', group: 'account', kind: 'select', options: [{ value: 0, label: '0 · Không' }, { value: 1, label: '1 · Có' }] },
  { name: 'Subscription  Length', label: 'Thời gian đăng ký', description: 'Tổng thời gian thuê bao đã đăng ký.', unit: 'tháng', group: 'account', kind: 'integer', min: 0 },
  { name: 'Charge  Amount', label: 'Mức cước', description: 'Nhóm mức cước thứ bậc, từ thấp nhất đến cao nhất.', unit: 'bậc 0–9', group: 'account', kind: 'select', options: Array.from({ length: 10 }, (_, value) => ({ value, label: `${value} · Bậc ${value}` })) },
  { name: 'Seconds of Use', label: 'Tổng thời lượng gọi', description: 'Tổng thời gian sử dụng cuộc gọi trong kỳ quan sát.', unit: 'giây', group: 'usage', kind: 'integer', min: 0 },
  { name: 'Frequency of use', label: 'Tần suất gọi', description: 'Tổng số cuộc gọi trong kỳ quan sát.', unit: 'cuộc gọi', group: 'usage', kind: 'integer', min: 0 },
  { name: 'Frequency of SMS', label: 'Tần suất SMS', description: 'Tổng số tin nhắn trong kỳ quan sát.', unit: 'tin nhắn', group: 'usage', kind: 'integer', min: 0 },
  { name: 'Distinct Called Numbers', label: 'Số liên lạc khác nhau', description: 'Số lượng số điện thoại khác nhau đã gọi; không nhập số điện thoại thật.', unit: 'số liên lạc', group: 'usage', kind: 'integer', min: 0 },
  { name: 'Age Group', label: 'Nhóm tuổi', description: 'Nhóm tuổi thứ bậc từ trẻ hơn đến lớn tuổi hơn.', unit: 'nhóm 1–5', group: 'profile', kind: 'select', options: Array.from({ length: 5 }, (_, index) => ({ value: index + 1, label: `${index + 1} · Nhóm ${index + 1}` })) },
  { name: 'Tariff Plan', label: 'Gói cước', description: 'Loại hình thanh toán của thuê bao.', unit: 'danh mục', group: 'account', kind: 'select', options: [{ value: 1, label: '1 · Trả theo mức sử dụng' }, { value: 2, label: '2 · Hợp đồng' }] },
  { name: 'Status', label: 'Trạng thái thuê bao', description: 'Trạng thái thuê bao trong cửa sổ quan sát.', unit: 'danh mục', group: 'account', kind: 'select', options: [{ value: 1, label: '1 · Đang hoạt động' }, { value: 2, label: '2 · Không hoạt động' }] },
  { name: 'Age', label: 'Tuổi khách hàng', description: 'Tuổi của khách hàng.', unit: 'năm', group: 'profile', kind: 'integer', min: 0 },
  { name: 'Customer Value', label: 'Giá trị khách hàng', description: 'Giá trị khách hàng do bộ dữ liệu tính; công thức chính xác chưa được công bố.', unit: 'giá trị tính toán', group: 'profile', kind: 'float', min: 0 },
] as const;

export const PUBLISHED_METRICS = {
  validation: { prAuc: 0.76007, averagePrecision: 0.761101, rocAuc: 0.936493, brier: 0.069941 },
  test: { prAuc: 0.796582, averagePrecision: 0.798105, rocAuc: 0.949951, brier: 0.062798, precision: 0.678261, recall: 0.787879, f1: 0.728972 },
} as const;
