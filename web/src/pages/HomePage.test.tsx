import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import App from '../App';
import { renderAt } from '../test/render';

describe('HomePage', () => {
  it('renders the project introduction and prediction link', () => {
    renderAt(<App />);
    expect(screen.getByRole('heading', { name: /Nhìn thấy tín hiệu rời mạng/i })).toBeInTheDocument();
    expect(screen.getByText(/Iranian Churn Dataset/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Bắt đầu dự đoán/i })).toHaveAttribute('href', '/predict');
  });
});
