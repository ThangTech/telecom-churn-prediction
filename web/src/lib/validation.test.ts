import { describe, expect, it } from 'vitest';
import { createEmptyFormValues, validateFeature, validateForm } from './validation';

describe('feature validation', () => {
  it('requires every one of the 13 frozen features', () => {
    expect(Object.keys(validateForm(createEmptyFormValues()))).toHaveLength(13);
  });

  it('rejects invalid integer, negative and categorical values', () => {
    expect(validateFeature('Age', '20.5')).toMatch(/số nguyên/i);
    expect(validateFeature('Seconds of Use', '-1')).toMatch(/0/);
    expect(validateFeature('Age Group', '6')).toMatch(/miền hợp lệ/i);
  });

  it('allows a non-negative floating Customer Value', () => {
    expect(validateFeature('Customer Value', '42.75')).toBeUndefined();
  });
});
