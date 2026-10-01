export type CapacityMode = 'LOW' | 'MEDIUM' | 'HIGH';

export type FeatureName =
  | 'Call  Failure'
  | 'Complains'
  | 'Subscription  Length'
  | 'Charge  Amount'
  | 'Seconds of Use'
  | 'Frequency of use'
  | 'Frequency of SMS'
  | 'Distinct Called Numbers'
  | 'Age Group'
  | 'Tariff Plan'
  | 'Status'
  | 'Age'
  | 'Customer Value';

export type ChurnFeatures = Record<FeatureName, number>;

export interface ChurnScoreRequest {
  features: ChurnFeatures;
  capacity_mode: CapacityMode;
}

export type PriorityGroup = 'HIGH' | 'MEDIUM' | 'EXTENDED' | 'NOT_PRIORITIZED';

export interface ChurnScoreResponse {
  churn_probability: number;
  predicted_churn: boolean;
  priority_group: PriorityGroup;
  threshold: number;
  capacity_mode: CapacityMode;
  model_version?: string;
  request_id?: string;
  source?: 'api' | 'mock';
}

export interface FeatureDefinition {
  name: FeatureName;
  label: string;
  description: string;
  unit: string;
  group: 'usage' | 'account' | 'profile';
  kind: 'integer' | 'float' | 'select';
  min?: number;
  max?: number;
  options?: ReadonlyArray<{ value: number; label: string }>;
}
