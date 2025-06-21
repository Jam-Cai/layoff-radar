
import React from 'react';
import { Card } from '@/components/ui/card';
import { ArrowUp, ArrowDown } from 'lucide-react';

interface Factor {
  name: string;
  value: number;
}

interface FactorCardsProps {
  factors: Factor[];
}

const FactorCards: React.FC<FactorCardsProps> = ({ factors }) => {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {factors.map((factor, index) => (
        <Card
          key={index}
          className="p-4 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-gray-200 dark:border-gray-700 rounded-xl hover:shadow-lg transition-all duration-200"
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h4 className="font-medium text-gray-900 dark:text-white text-sm mb-1">
                {factor.name}
              </h4>
              <div className="flex items-center space-x-2">
                <div className={`flex items-center ${factor.value >= 0 ? 'text-red-500' : 'text-green-500'}`}>
                  {factor.value >= 0 ? (
                    <ArrowUp className="h-4 w-4 mr-1" />
                  ) : (
                    <ArrowDown className="h-4 w-4 mr-1" />
                  )}
                  <span className="font-semibold">
                    {Math.abs(factor.value * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
            <div className={`w-2 h-12 rounded-full ${factor.value >= 0 ? 'bg-red-500' : 'bg-green-500'}`}>
              <div
                className="w-full bg-current rounded-full transition-all duration-500"
                style={{ height: `${Math.abs(factor.value) * 100}%` }}
              />
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
};

export default FactorCards;
