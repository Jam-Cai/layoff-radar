
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

  // Calculate the stroke dash array for the semi-circle
  const radius = 90;
  const circumference = Math.PI * radius;
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (risk / 100) * circumference;

  return (
    <div className="text-center">
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{company}</h3>
      <div className="relative w-64 h-32 mx-auto mb-4">
        <svg
          className="w-full h-full transform -rotate-90"
          viewBox="0 0 200 100"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Background arc */}
          <path
            d="M 10 90 A 90 90 0 0 1 190 90"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-gray-200 dark:text-gray-700"
          />
          {/* Progress arc */}
          <path
            d="M 10 90 A 90 90 0 0 1 190 90"
            fill="none"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            className={`bg-gradient-to-r ${getRiskColorBg(risk)} transition-all duration-1000 ease-out`}
            style={{
              stroke: risk < 40 ? '#10b981' : risk < 70 ? '#f59e0b' : '#ef4444'
            }}
          />
        </svg>
        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className={`text-4xl md:text-5xl font-bold ${getRiskColor(risk)} mb-1`}>
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
