import { CAPACITY_THRESHOLDS } from '../config/model';
import type { ChurnScoreRequest, ChurnScoreResponse, PriorityGroup } from '../types/churn';

const REQUEST_TIMEOUT_MS = 10_000;

export class ChurnApiError extends Error {
  constructor(
    message: string,
    public readonly kind: 'validation' | 'server' | 'network' | 'timeout' | 'malformed',
    public readonly status?: number,
  ) {
    super(message);
    this.name = 'ChurnApiError';
  }
}

function priorityForProbability(probability: number): PriorityGroup {
  if (probability >= CAPACITY_THRESHOLDS.LOW) return 'HIGH';
  if (probability >= CAPACITY_THRESHOLDS.MEDIUM) return 'MEDIUM';
  if (probability >= CAPACITY_THRESHOLDS.HIGH) return 'EXTENDED';
  return 'NOT_PRIORITIZED';
}

function isCapacityMode(value: unknown): value is ChurnScoreResponse['capacity_mode'] {
  return value === 'LOW' || value === 'MEDIUM' || value === 'HIGH';
}

function isPriorityGroup(value: unknown): value is PriorityGroup {
  return value === 'HIGH' || value === 'MEDIUM' || value === 'EXTENDED' || value === 'NOT_PRIORITIZED';
}

function parseResponse(value: unknown, request: ChurnScoreRequest): ChurnScoreResponse {
  if (!value || typeof value !== 'object') throw new ChurnApiError('API trả về dữ liệu không đúng cấu trúc.', 'malformed');
  const item = value as Record<string, unknown>;
  if (
    typeof item.churn_probability !== 'number' ||
    !Number.isFinite(item.churn_probability) ||
    item.churn_probability < 0 ||
    item.churn_probability > 1 ||
    typeof item.predicted_churn !== 'boolean' ||
    typeof item.threshold !== 'number' ||
    !Number.isFinite(item.threshold) ||
    !isCapacityMode(item.capacity_mode) ||
    !isPriorityGroup(item.priority_group)
  ) {
    throw new ChurnApiError('API trả về dữ liệu không đúng cấu trúc đã thống nhất.', 'malformed');
  }
  const parsed = { ...item, source: 'api' } as ChurnScoreResponse;
  const expectedThreshold = CAPACITY_THRESHOLDS[parsed.capacity_mode];
  if (
    parsed.capacity_mode !== request.capacity_mode ||
    Math.abs(parsed.threshold - expectedThreshold) > 0.000001 ||
    parsed.predicted_churn !== (parsed.churn_probability >= parsed.threshold) ||
    parsed.priority_group !== priorityForProbability(parsed.churn_probability)
  ) {
    throw new ChurnApiError('API trả về kết quả không nhất quán với mode hoặc ngưỡng đã đóng băng.', 'malformed');
  }
  return parsed;
}

async function mockScore(request: ChurnScoreRequest): Promise<ChurnScoreResponse> {
  await new Promise((resolve) => setTimeout(resolve, 450));
  const probability = 0.62;
  const threshold = CAPACITY_THRESHOLDS[request.capacity_mode];
  return {
    churn_probability: probability,
    predicted_churn: probability >= threshold,
    priority_group: priorityForProbability(probability),
    threshold,
    capacity_mode: request.capacity_mode,
    model_version: 'development-mock',
    request_id: 'mock-local-only',
    source: 'mock',
  };
}

export async function scoreChurn(request: ChurnScoreRequest): Promise<ChurnScoreResponse> {
  const useMock = import.meta.env.DEV && import.meta.env.VITE_USE_MOCK_API === 'true';
  if (useMock) return mockScore(request);

  const baseUrl = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '');
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${baseUrl}/api/churn-score`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
      signal: controller.signal,
    });

    if (response.status === 400 || response.status === 422) {
      throw new ChurnApiError('Backend từ chối dữ liệu đầu vào. Hãy kiểm tra lại các trường đã nhập.', 'validation', response.status);
    }
    if (response.status >= 500) {
      throw new ChurnApiError('Dịch vụ dự đoán đang gặp lỗi. Vui lòng thử lại sau.', 'server', response.status);
    }
    if (!response.ok) {
      throw new ChurnApiError(`Không thể hoàn tất yêu cầu dự đoán (HTTP ${response.status}).`, 'server', response.status);
    }

    let payload: unknown;
    try {
      payload = await response.json();
    } catch {
      throw new ChurnApiError('API không trả về JSON hợp lệ.', 'malformed');
    }
    return parseResponse(payload, request);
  } catch (error) {
    if (error instanceof ChurnApiError) throw error;
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new ChurnApiError('Yêu cầu đã quá thời gian chờ 10 giây.', 'timeout');
    }
    throw new ChurnApiError('Không kết nối được API. Hãy kiểm tra backend và VITE_API_BASE_URL.', 'network');
  } finally {
    window.clearTimeout(timeout);
  }
}
