import { FEATURE_DEFINITIONS } from '../config/model';
import type { ChurnFeatures, FeatureName } from '../types/churn';

export type FormValues = Record<FeatureName, string>;
export type FormErrors = Partial<Record<FeatureName, string>>;

export const createEmptyFormValues = (): FormValues =>
  Object.fromEntries(FEATURE_DEFINITIONS.map((feature) => [feature.name, ''])) as FormValues;

export function validateFeature(name: FeatureName, rawValue: string): string | undefined {
  const definition = FEATURE_DEFINITIONS.find((feature) => feature.name === name);
  if (!definition) return 'Thuộc tính không được hỗ trợ.';
  if (rawValue.trim() === '') return 'Trường này là bắt buộc.';

  const value = Number(rawValue);
  if (!Number.isFinite(value)) return 'Vui lòng nhập một giá trị số hợp lệ.';
  if (definition.kind !== 'float' && !Number.isInteger(value)) return 'Vui lòng nhập số nguyên.';
  if (definition.min !== undefined && value < definition.min) return `Giá trị phải từ ${definition.min} trở lên.`;
  if (definition.max !== undefined && value > definition.max) return `Giá trị không được vượt quá ${definition.max}.`;
  if (definition.options && !definition.options.some((option) => option.value === value)) return 'Giá trị không thuộc miền hợp lệ.';
  return undefined;
}

export function validateForm(values: FormValues): FormErrors {
  return Object.fromEntries(
    FEATURE_DEFINITIONS.flatMap((feature) => {
      const error = validateFeature(feature.name, values[feature.name]);
      return error ? [[feature.name, error]] : [];
    }),
  ) as FormErrors;
}

export function toChurnFeatures(values: FormValues): ChurnFeatures {
  return Object.fromEntries(
    FEATURE_DEFINITIONS.map((feature) => [feature.name, Number(values[feature.name])]),
  ) as ChurnFeatures;
}
