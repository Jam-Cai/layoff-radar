import { useState, useEffect } from 'react';
import { io, Socket } from 'socket.io-client';

interface LayoffData {
  risk_level: number;
  explanation: string;
}

interface StatusMessage {
  message: string;
}

interface AnalysisComplete {
  risk_level: number;
  explanation: string;
  complete: boolean;
}

interface ErrorMessage {
  message: string;
}

export const useRiskData = () => {
  const [data, setData] = useState<LayoffData | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('');
  const [socket, setSocket] = useState<Socket | null>(null);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

  useEffect(() => {
    // Initialize Socket.IO connection
    const newSocket = io(API_BASE_URL, {
      transports: ['websocket', 'polling']
    });

    newSocket.on('connect', () => {
      console.log('Connected to server');
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from server');
    });

    newSocket.on('status', (data: StatusMessage) => {
      setStatus(data.message);
    });

    newSocket.on('analysis_complete', (data: AnalysisComplete) => {
      setData({
        risk_level: data.risk_level,
        explanation: data.explanation,
      });
      setLoading(false);
      setStatus('');
    });

    newSocket.on('error', (data: ErrorMessage) => {
      console.error('Socket error:', data.message);
      setLoading(false);
      setStatus('');
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [API_BASE_URL]);

  const fetchRiskData = async (company: string) => {
    if (!socket) {
      console.error('Socket not connected');
      return;
    }

    setLoading(true);
    setStatus('');
    setData(null);

    socket.emit('analyze_company', { company_name: company });
  };

  return { data, loading, status, fetchRiskData };
};