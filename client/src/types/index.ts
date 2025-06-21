
export interface Factor {
  name: string;
  value: number;
}

export interface HistoryPoint {
  date: string;
  risk: number;
}

export interface RiskData {
  company: string;
  risk: number;
  top_factors: Factor[];
  history: HistoryPoint[];
  explanation: string;
}
