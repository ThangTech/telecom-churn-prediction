import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import App from '../App';
import { renderAt } from '../test/render';

describe('ModelCardPage', () => {
  it('shows only the frozen model facts and separates validation from test', () => {
    renderAt(<App />, '/model-card');
    expect(screen.getByRole('heading', { name: 'Logistic Regression' })).toBeInTheDocument();
    expect(screen.getByText('0.796582')).toBeInTheDocument();
    expect(screen.getByText(/Test không dùng để tuning/i)).toBeInTheDocument();
    expect(screen.getByText(/khả năng phản hồi ưu đãi chăm sóc/i)).toBeInTheDocument();
  });
});
