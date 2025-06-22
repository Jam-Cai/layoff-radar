import { useState, useEffect, useRef } from 'react';
import { io, Socket } from 'socket.io-client';

interface LayoffData {
  risk_level: number;
  explanation: string;
  key_points?: [string, string][];
}

interface AnalysisStatus {
  message: string;
}

interface AnalysisError {
  message: string;
}

interface AnalysisComplete {
  risk_level: number;
  explanation: string;
  key_points: [string, string][];
  complete: boolean;
}

export const useRiskData = () => {
  const [data, setData] = useState<LayoffData | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('');
  const [progress, setProgress] = useState<number>(0);
  const socketRef = useRef<Socket | null>(null);

  const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'http://127.0.0.1:8000';

  const connectSocket = () => {
    if (!socketRef.current) {
      socketRef.current = io(SOCKET_URL, {
        transports: ['websocket', 'polling'],
        autoConnect: true,
      });

      // Socket event listeners
      socketRef.current.on('connect', () => {
        console.log('Connected to WebSocket server');
      });

      socketRef.current.on('disconnect', () => {
        console.log('Disconnected from WebSocket server');
      });

      socketRef.current.on('status', (data: AnalysisStatus) => {
        setStatus(data.message);
        // Update progress based on status message
        if (data.message.includes('Step 1')) {
          setProgress(20);
        } else if (data.message.includes('Step 2')) {
          setProgress(40);
        } else if (data.message.includes('Step 3')) {
          setProgress(60);
        } else if (data.message.includes('Step 4')) {
          setProgress(80);
        } else if (data.message.includes('Step 5')) {
          setProgress(90);
        }
      });

      socketRef.current.on('analysis_complete', (data: AnalysisComplete) => {
        setData({
          risk_level: Math.floor(data.risk_level),
          explanation: data.explanation,
          key_points: data.key_points,
        });
        setLoading(false);
        setStatus('');
        setProgress(100);
      });

      socketRef.current.on('error', (data: AnalysisError) => {
        console.error('Analysis error:', data.message);
        setLoading(false);
        setStatus('');
        setProgress(0);
      });
    }
  };

  const disconnectSocket = () => {
    if (socketRef.current) {
      socketRef.current.disconnect();
      socketRef.current = null;
    }
  };

  const fetchRiskData = async (company: string) => {
    try {
      setLoading(true);
      setStatus('');
      setData(null);
      setProgress(0);

      // Ensure socket is connected
      connectSocket();

      // Emit the analysis request
      socketRef.current?.emit('analyze_company', { company_name: company });

    } catch (error) {
      console.error('Error starting analysis:', error);
      setLoading(false);
      setStatus('');
      setProgress(0);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    connectSocket();
    
    return () => {
      disconnectSocket();
    };
  }, []);

  return { data, loading, status, progress, fetchRiskData };
};