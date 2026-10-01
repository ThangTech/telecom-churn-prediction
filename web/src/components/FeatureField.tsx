import type { FeatureDefinition } from '../types/churn';

interface FeatureFieldProps {
  feature: FeatureDefinition;
  value: string;
  error?: string;
  onChange: (value: string) => void;
  onBlur: () => void;
}

export function FeatureField({ feature, value, error, onChange, onBlur }: FeatureFieldProps) {
  const id = `field-${feature.name.replaceAll(' ', '-').toLowerCase()}`;
  const describedBy = `${id}-help${error ? ` ${id}-error` : ''}`;

  return (
    <div className={`field ${error ? 'field-invalid' : ''}`}>
      <label htmlFor={id}>
        <span>{feature.label} <b aria-hidden="true">*</b></span>
        <small>{feature.name}</small>
      </label>
      {feature.kind === 'select' ? (
        <select
          id={id}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          onBlur={onBlur}
          aria-invalid={Boolean(error)}
          aria-describedby={describedBy}
        >
          <option value="">Chọn giá trị</option>
          {feature.options?.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
        </select>
      ) : (
        <div className="input-with-unit">
          <input
            id={id}
            type="number"
            inputMode={feature.kind === 'integer' ? 'numeric' : 'decimal'}
            step={feature.kind === 'integer' ? 1 : 'any'}
            min={feature.min}
            max={feature.max}
            value={value}
            onChange={(event) => onChange(event.target.value)}
            onBlur={onBlur}
            aria-invalid={Boolean(error)}
            aria-describedby={describedBy}
            placeholder="Nhập giá trị"
          />
          <span>{feature.unit}</span>
        </div>
      )}
      <p id={`${id}-help`} className="field-help">{feature.description}</p>
      {error && <p id={`${id}-error`} className="field-error" role="alert">{error}</p>}
    </div>
  );
}
