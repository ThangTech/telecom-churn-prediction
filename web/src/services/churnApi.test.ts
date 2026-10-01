import { afterEach, describe, expect, it, vi } from 'vitest';
import { scoreChurn } from './churnApi';
import type { ChurnScoreRequest } from '../types/churn';

const request = {
  capacity_mode: 'MEDIUM',
  features: {
    'Call  Failure': 1, Complains: 0, 'Subscription  Length': 24, 'Charge  Amount': 2,
    'Seconds of Use': 1000, 'Frequency of use': 80, 'Frequency of SMS': 12,
    'Distinct Called Numbers': 20, 'Age Group': 3, 'Tariff Plan': 1, Status: 1, Age: 35,
    'Customer Value': 42.75,
  },
} satisfies ChurnScoreRequest;

describe('churnApi', () => {
  afterEach(() => vi.unstubAllGlobals());

  it('rejects malformed API responses', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ probability: 0.4 }), { status: 200, headers: { 'Content-Type': 'application/json' } })));
    await expect(scoreChurn(request)).rejects.toMatchObject({ kind: 'malformed' });
  });

  it('maps HTTP 422 to a validation error', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('{}', { status: 422 })));
    await expect(scoreChurn(request)).rejects.toMatchObject({ kind: 'validation', status: 422 });
  });
});
