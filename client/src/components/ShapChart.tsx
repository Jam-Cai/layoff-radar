import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface Factor {
  name: string;
  value: number;
}

interface ShapChartProps {
  factors: Factor[];
}

const ShapChart: React.FC<ShapChartProps> = ({ factors }) => {
  const data = factors.map(factor => ({
    name: factor.name,
    value: factor.value,
    absValue: Math.abs(factor.value)
  }));

  interface CustomTooltipProps {
    active?: boolean;
    payload?: { value: number }[];
    label?: string;
  }

  const CustomTooltip = ({ active, payload, label }: CustomTooltipProps) => {
    if (active && payload && payload.length) {
      const value = payload[0].value;
      return (
        <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="font-medium">{label}</p>
          <p className={`${value >= 0 ? 'text-red-500' : 'text-green-500'}`}>
            Impact: {(value * 100).toFixed(1)}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-6">
        SHAP Factor Analysis
      </h3>
      {data.length > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={data}
            layout="horizontal"
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
            <XAxis
              type="number"
              domain={[-0.5, 0.5]}
              axisLine={false}
              tickLine={false}
              className="text-gray-600 dark:text-gray-400"
            />
            <YAxis
              type="category"
              dataKey="name"
              axisLine={false}
              tickLine={false}
              className="text-gray-600 dark:text-gray-400"
              width={120}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.value >= 0 ? '#ef4444' : '#10b981'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <div className="flex items-center justify-center h-[300px] text-gray-500">
          No factor data available to display.
        </div>
      )}
      <div className="mt-4 text-sm text-gray-600 dark:text-gray-400">
        <span className="inline-flex items-center mr-4">
          <div className="w-3 h-3 bg-red-500 rounded mr-2"></div>
          Increases Risk
        </span>
        <span className="inline-flex items-center">
          <div className="w-3 h-3 bg-green-500 rounded mr-2"></div>
          Decreases Risk
        </span>
      </div>
    </div>
  );
};

export default ShapChart;
