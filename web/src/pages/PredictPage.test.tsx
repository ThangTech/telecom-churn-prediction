import { act, fireEvent, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import App from '../App';
import { ChurnApiError } from '../services/churnApi';
import { renderAt } from '../test/render';
import type { ChurnScoreResponse } from '../types/churn';

const scoreChurnMock = vi.hoisted(() => vi.fn());
vi.mock('../services/churnApi', async (importOriginal) => {
  const original = await importOriginal<typeof import('../services/churnApi')>();
  return { ...original, scoreChurn: scoreChurnMock };
});

const apiResult: ChurnScoreResponse = {
  churn_probability: 0.62,
  predicted_churn: true,
  priority_group: 'HIGH',
  threshold: 0.3431830803885034,
  capacity_mode: 'MEDIUM',
  source: 'mock',
};

async function fillValidForm() {
  const user = userEvent.setup();
  await user.type(screen.getByLabelText(/Số lần cuộc gọi thất bại/i), '1');
  await user.selectOptions(screen.getByLabelText(/Có khiếu nại/i), '0');
  await user.type(screen.getByLabelText(/Thời gian đăng ký/i), '24');
  await user.selectOptions(screen.getByLabelText(/Mức cước/i), '2');
  await user.type(screen.getByLabelText(/Tổng thời lượng gọi/i), '1000');
  await user.type(screen.getByLabelText(/Tần suất gọi/i), '80');
  await user.type(screen.getByLabelText(/Tần suất SMS/i), '12');
  await user.type(screen.getByLabelText(/Số liên lạc khác nhau/i), '20');
  await user.selectOptions(screen.getByLabelText(/Nhóm tuổi/i), '3');
  await user.selectOptions(screen.getByLabelText(/Gói cước/i), '1');
  await user.selectOptions(screen.getByLabelText(/Trạng thái thuê bao/i), '1');
  await user.type(screen.getByLabelText(/Tuổi khách hàng/i), '35');
  await user.type(screen.getByLabelText(/Giá trị khách hàng/i), '42.75');
  return user;
}

describe('PredictPage', () => {
  beforeEach(() => {
    scoreChurnMock.mockReset();
  });

  it('shows exactly the 13 frozen feature fields and excludes technical/target fields', () => {
    const { container } = renderAt(<App />, '/predict');
    expect(container.querySelectorAll('[aria-describedby^="field-"]')).toHaveLength(13);
    expect(screen.queryByLabelText(/^Churn$/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/^row_id$/i)).not.toBeInTheDocument();
  });

  it('does not submit missing data and renders inline validation errors', async () => {
    renderAt(<App />, '/predict');
    await userEvent.click(screen.getByRole('button', { name: /Dự đoán nguy cơ rời mạng/i }));
    expect(scoreChurnMock).not.toHaveBeenCalled();
    expect(screen.getByText(/Có 13 trường cần kiểm tra/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Trường này là bắt buộc/i)).toHaveLength(13);
  });

  it('maps valid values to the expected request schema and shows the mock result', async () => {
    scoreChurnMock.mockResolvedValue(apiResult);
    renderAt(<App />, '/predict');
    const user = await fillValidForm();
    await user.click(screen.getByRole('button', { name: /Dự đoán nguy cơ rời mạng/i }));

    await waitFor(() => expect(scoreChurnMock).toHaveBeenCalledTimes(1));
    expect(scoreChurnMock).toHaveBeenCalledWith({
      capacity_mode: 'MEDIUM',
      features: {
        'Call  Failure': 1,
        Complains: 0,
        'Subscription  Length': 24,
        'Charge  Amount': 2,
        'Seconds of Use': 1000,
        'Frequency of use': 80,
        'Frequency of SMS': 12,
        'Distinct Called Numbers': 20,
        'Age Group': 3,
        'Tariff Plan': 1,
        Status: 1,
        Age: 35,
        'Customer Value': 42.75,
      },
    });
    const result = await screen.findByRole('region', { name: /Kết quả dự đoán/i });
    expect(within(result).getByText('62.0%')).toBeInTheDocument();
    expect(within(result).getByText('Ưu tiên cao')).toBeInTheDocument();
    expect(within(result).getByText(/DỮ LIỆU MÔ PHỎNG/i)).toBeInTheDocument();
  });

  it('keeps the UI available when the API is down', async () => {
    let rejectRequest: (reason: unknown) => void = () => undefined;
    scoreChurnMock.mockImplementation(() => new Promise((_, reject) => { rejectRequest = reject; }));
    renderAt(<App />, '/predict');
    const user = await fillValidForm();
    await user.click(screen.getByRole('button', { name: /Dự đoán nguy cơ rời mạng/i }));
    await act(async () => rejectRequest(new ChurnApiError('Không kết nối được API.', 'network')));
    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent(/Không thể dự đoán.*Không kết nối được API/i);
    expect(screen.getByRole('button', { name: /Dự đoán nguy cơ rời mạng/i })).toBeEnabled();
  });

  it('disables duplicate submission while loading', async () => {
    let resolveRequest: (value: ChurnScoreResponse) => void = () => undefined;
    scoreChurnMock.mockImplementation(() => new Promise((resolve) => { resolveRequest = resolve; }));
    renderAt(<App />, '/predict');
    await fillValidForm();
    const submit = screen.getByRole('button', { name: /Dự đoán nguy cơ rời mạng/i });
    fireEvent.submit(submit.closest('form')!);
    await waitFor(() => expect(screen.getByRole('button', { name: /Đang dự đoán/i })).toBeDisabled());
    fireEvent.click(screen.getByRole('button', { name: /Đang dự đoán/i }));
    expect(scoreChurnMock).toHaveBeenCalledTimes(1);
    await act(async () => resolveRequest(apiResult));
    await screen.findByText('62.0%');
  });
});
