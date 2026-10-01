import { screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import App from '../App';
import { renderAt } from '../test/render';

describe('DashboardPage', () => {
  it('labels safe demo data and sorts probabilities descending', () => {
    renderAt(<App />, '/dashboard');
    expect(screen.getByText(/Không phải tập test và không chứa thông tin cá nhân/i)).toBeInTheDocument();
    expect(screen.getByText(/Không phải metric hiệu năng/i)).toBeInTheDocument();
    const rows = screen.getAllByRole('row').slice(1);
    expect(within(rows[0]).getByText('DEMO-1042')).toBeInTheDocument();
    expect(within(rows[0]).getByText('82.0%')).toBeInTheDocument();
  });
});
