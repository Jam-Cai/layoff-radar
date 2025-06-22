import React from 'react';

interface RiskGaugeProps {
  risk: number;
  company: string;
}

const RiskGauge: React.FC<RiskGaugeProps> = ({ risk, company }) => {
  const getRiskColor = (risk: number) => {
    if (risk < 40) return 'text-green-500';
    if (risk < 70) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getRiskColorBg = (risk: number) => {
    if (risk < 40) return 'from-green-400 to-green-600';
    if (risk < 70) return 'from-yellow-400 to-yellow-600';
    return 'from-red-400 to-red-600';
  };

  const getRiskLevel = (risk: number) => {
    if (risk < 40) return 'Low Risk';
    if (risk < 70) return 'Medium Risk';
    return 'High Risk';
  };

  const getStrokeColor = (risk: number) => {
    if (risk < 40) return '#10b981'; // green
    if (risk < 70) return '#f59e0b'; // yellow
    return '#ef4444'; // red
  };

  // Calculate the stroke dash array for the full circle
  const radius = 50;
  const center = 80;
  const circumference = 2 * Math.PI * radius; // Full circle circumference
  const strokeDashoffset = circumference - (risk / 100) * circumference;

  return (
    <div className="text-center">
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{company}</h3>
      <div className="relative w-48 h-48 mx-auto mb-4">
        <svg
          className="w-full h-full transform -rotate-90"
          viewBox="0 0 160 160"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Background circle */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-gray-200 dark:text-gray-700"
          />
          {/* Progress circle */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke={getStrokeColor(risk)}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className={`text-3xl md:text-4xl font-bold ${getRiskColor(risk)} mb-1`}>
            {risk}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            {getRiskLevel(risk)}
          </div>
        </div>
      </div>
      <div className="text-sm text-gray-600 dark:text-gray-400">
        Layoff Risk Score
      </div>
    </div>
  );
};

export default RiskGauge;
