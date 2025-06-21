
import React from 'react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';

interface HistoryPoint {
  date: string;
  risk: number;
}

interface SparklineChartProps {
  history: HistoryPoint[];
}

const SparklineChart: React.FC<SparklineChartProps> = ({ history }) => {
  const getRiskColor = (risk: number) => {
    if (risk < 40) return '#10b981';
    if (risk < 70) return '#f59e0b';
    return '#ef4444';
  };

  const currentRisk = history[history.length - 1]?.risk || 0;
  const previousRisk = history[history.length - 2]?.risk || 0;
  const change = currentRisk - previousRisk;

  return (
    <div className="h-full flex flex-col">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        30-Day Trend
      </h3>
      <div className="flex-1 mb-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={history}>
            <Line
              type="monotone"
              dataKey="risk"
              stroke={getRiskColor(currentRisk)}
              strokeWidth={3}
              dot={false}
              activeDot={{ r: 4, fill: getRiskColor(currentRisk) }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="text-center">
        <div className={`text-sm font-medium ${change >= 0 ? 'text-red-500' : 'text-green-500'}`}>
          {change >= 0 ? '+' : ''}{change.toFixed(1)} from yesterday
        </div>
        <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
          {history.length} day history
        </div>
      </div>
    </div>
  );
};

export default SparklineChart;
