import { useState } from 'react';

interface LayoffData {
  risk_level: number;
  explanation: string;
}

export const useRiskData = () => {
  const [data, setData] = useState<LayoffData | null>(null);
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'ws://127.0.0.1:8000';

  const fetchRiskData = async (company: string) => {
    setLoading(true);
    const socket = new WebSocket(`${API_BASE_URL}/layoffs/${encodeURIComponent(company)}`);

    let explanation = "";
    let riskLevel: number | null = null;

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.risk_level !== undefined) {
        riskLevel = message.risk_level;
      }

      if (message.partial_explanation) {
        explanation += message.partial_explanation;
      }

      if (message.done) {
        setData({
          risk_level: riskLevel ?? 0,
          explanation,
        });
        setLoading(false);
        socket.close();
      }
    };

    socket.onerror = () => {
      console.error("WebSocket error");
      setLoading(false);
      socket.close();
    };
  };

  return { data, loading, fetchRiskData };
};