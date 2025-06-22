import { useState, useEffect, useRef } from 'react';

interface LayoffData {
  risk_level: number;
  explanation: string;
}

interface AnalysisStatus {
  status: 'processing' | 'complete' | 'error';
  message: string;
  progress?: number;
  risk_level?: number;
  explanation?: string;
}

interface AnalysisResponse {
  analysis_id: string;
  message: string;
  status: string;
}

export const useRiskData = () => {
  const [data, setData] = useState<LayoffData | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('');
  const [progress, setProgress] = useState<number>(0);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

  const stopPolling = () => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
      pollingIntervalRef.current = null;
    }
  };

  const pollAnalysisStatus = async (analysisId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/analysis/${analysisId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch analysis status');
      }

      const statusData: AnalysisStatus = await response.json();
      
      setStatus(statusData.message);
      if (statusData.progress !== undefined) {
        setProgress(statusData.progress);
      }

      if (statusData.status === 'complete') {
        setData({
          risk_level: statusData.risk_level!,
          explanation: statusData.explanation!,
        });
        setLoading(false);
        setStatus('');
        setProgress(0);
        stopPolling();
      } else if (statusData.status === 'error') {
        console.error('Analysis error:', statusData.message);
        setLoading(false);
        setStatus('');
        setProgress(0);
        stopPolling();
      }
    } catch (error) {
      console.error('Error polling analysis status:', error);
      setLoading(false);
      setStatus('');
      setProgress(0);
      stopPolling();
    }
  };

  const fetchRiskData = async (company: string) => {
    try {
      setLoading(true);
      setStatus('');
      setData(null);
      setProgress(0);
      stopPolling();

      // Start analysis
      const response = await fetch(`${API_BASE_URL}/analyze/${encodeURIComponent(company)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to start analysis');
      }

      const analysisResponse: AnalysisResponse = await response.json();
      
      // Start polling for status updates
      pollingIntervalRef.current = setInterval(() => {
        pollAnalysisStatus(analysisResponse.analysis_id);
      }, 1000); // Poll every second

      // Initial status check
      await pollAnalysisStatus(analysisResponse.analysis_id);

    } catch (error) {
      console.error('Error starting analysis:', error);
      setLoading(false);
      setStatus('');
      setProgress(0);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, []);

  return { data, loading, status, progress, fetchRiskData };
};