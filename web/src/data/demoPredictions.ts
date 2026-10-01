import type { PriorityGroup } from '../types/churn';

export interface DemoPrediction {
  customerId: string;
  probability: number;
  priority: PriorityGroup;
  status: 'Cần xem xét' | 'Theo dõi';
}

export const DEMO_PREDICTIONS: readonly DemoPrediction[] = [
  { customerId: 'DEMO-1042', probability: 0.82, priority: 'HIGH', status: 'Cần xem xét' },
  { customerId: 'DEMO-1031', probability: 0.69, priority: 'HIGH', status: 'Cần xem xét' },
  { customerId: 'DEMO-1057', probability: 0.53, priority: 'HIGH', status: 'Cần xem xét' },
  { customerId: 'DEMO-1008', probability: 0.41, priority: 'MEDIUM', status: 'Cần xem xét' },
  { customerId: 'DEMO-1019', probability: 0.36, priority: 'MEDIUM', status: 'Cần xem xét' },
  { customerId: 'DEMO-1064', probability: 0.29, priority: 'EXTENDED', status: 'Theo dõi' },
  { customerId: 'DEMO-1026', probability: 0.21, priority: 'EXTENDED', status: 'Theo dõi' },
  { customerId: 'DEMO-1078', probability: 0.12, priority: 'NOT_PRIORITIZED', status: 'Theo dõi' },
] as const;
