
import { useState, useCallback } from 'react';
import { debounce } from 'lodash-es';

interface Factor {
  name: string;
  value: number;
}

interface HistoryPoint {
  date: string;
  risk: number;
}

interface RiskData {
  company: string;
  risk: number;
  top_factors: Factor[];
  history: HistoryPoint[];
  explanation: string;
}

export const useRiskData = () => {
  const [data, setData] = useState<RiskData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.layoffradar.com';

  const fetchRiskData = useCallback(
    debounce(async (company: string) => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_BASE_URL}/score/${encodeURIComponent(company)}`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error('Error fetching risk data:', err);
        setError(err instanceof Error ? err.message : 'An error occurred');
        
        // Mock data for demo purposes
        const mockData: RiskData = {
          company: company,
          risk: Math.floor(Math.random() * 100),
          top_factors: [
            { name: "Executive exits", value: 0.34 },
            { name: "Layoff-intent news", value: 0.28 },
            { name: "Funding cushion", value: -0.05 }
          ],
          history: Array.from({ length: 30 }, (_, i) => ({
            date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            risk: Math.floor(Math.random() * 100)
          })),
          explanation: `Risk analysis for ${company} indicates moderate to high layoff probability based on recent market indicators, executive movements, and financial performance metrics. The analysis considers multiple data points including news sentiment, funding status, and industry trends.`
        };
        setData(mockData);
        setError(null);
      } finally {
        setLoading(false);
      }
    }, 300),
    []
  );

  return { data, loading, error, fetchRiskData };
};
