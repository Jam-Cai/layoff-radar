
import React, { useState } from 'react';
import { Moon, Sun, Search, ChevronDown } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from '@/hooks/use-toast';
import RiskGauge from '@/components/RiskGauge';
import FactorCards from '@/components/FactorCards';
import ShapChart from '@/components/ShapChart';
import SparklineChart from '@/components/SparklineChart';
import { useRiskData } from '@/utils/api';
import { getRecentLookups, saveToRecentLookups } from '@/lib/storage';

const Dashboard = () => {
  const [company, setCompany] = useState('');
  const [searchValue, setSearchValue] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [isExplanationOpen, setIsExplanationOpen] = useState(false);
  const [recentLookups, setRecentLookups] = useState<string[]>(getRecentLookups());

  const { data, loading, fetchRiskData } = useRiskData();

  const handleSearch = async (searchCompany: string) => {
    if (!searchCompany.trim()) return;
    
    try {
      await fetchRiskData(searchCompany);
      setCompany(searchCompany);
      const updated = saveToRecentLookups(searchCompany);
      setRecentLookups(updated);
      setSearchValue('');
    } catch (err) {
      toast({
        title: "Error",
        description: "Company not found or API error occurred",
        variant: "destructive"
      });
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch(searchValue);
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'dark bg-gray-900' : 'bg-gradient-to-br from-slate-50 to-blue-50'}`}>
      {/* Header */}
      <header className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">LR</span>
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                Layoff Radar
              </h1>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleDarkMode}
              className="p-2"
              aria-label="Toggle dark mode"
            >
              {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <section className="text-center mb-12">
          <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
            <h2 className="text-4xl md:text-6xl font-bold mb-4">
              Know Before the Notice
            </h2>
          </div>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
            AI-powered layoff risk analysis for companies. Get insights into potential workforce changes before they happen.
          </p>

          {/* Search Bar */}
          <div className="max-w-md mx-auto mb-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <Input
                type="text"
                placeholder="Enter company name or ticker..."
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onKeyPress={handleKeyPress}
                className="pl-10 pr-4 py-3 text-lg bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-gray-200 dark:border-gray-700 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                aria-label="Company search"
              />
              <Button
                onClick={() => handleSearch(searchValue)}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-indigo-500 hover:bg-indigo-600 rounded-lg px-4"
                disabled={loading}
              >
                Search
              </Button>
            </div>
          </div>

          {/* Recent Lookups */}
          {recentLookups.length > 0 && (
            <div className="flex flex-wrap justify-center gap-2 mb-8">
              <span className="text-sm text-gray-500 dark:text-gray-400 mr-2">Recent:</span>
              {recentLookups.map((lookup, index) => (
                <button
                  key={index}
                  onClick={() => handleSearch(lookup)}
                  className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-full transition-colors"
                >
                  {lookup}
                </button>
              ))}
            </div>
          )}
        </section>

        {/* Dashboard Content */}
        {loading && (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div className="col-span-full">
              <Skeleton className="h-64 w-full rounded-xl" />
            </div>
            <Skeleton className="h-32 rounded-xl" />
            <Skeleton className="h-32 rounded-xl" />
            <Skeleton className="h-32 rounded-xl" />
          </div>
        )}

        {data && !loading && (
          <div className="space-y-8">
            {/* Risk Gauge and Sparkline */}
            <div className="grid gap-6 lg:grid-cols-3">
              <div className="lg:col-span-2">
                <Card className="p-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-gray-200 dark:border-gray-700 rounded-xl">
                  <RiskGauge risk={data.risk_level} company={company} />
                </Card>
              </div>
              <div>
                <Card className="p-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-gray-200 dark:border-gray-700 rounded-xl h-full">
                  <SparklineChart history={null} />
                </Card>
              </div>
            </div>

            {/* Factor Cards
            <FactorCards factors={data.top_factors} />

            SHAP Chart
            <Card className="p-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-gray-200 dark:border-gray-700 rounded-xl">
              <ShapChart factors={data.top_factors} />
            </Card> */}

            {/* Explanation */}
            <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md border-gray-200 dark:border-gray-700 rounded-xl">
              <Collapsible open={isExplanationOpen} onOpenChange={setIsExplanationOpen}>
                <CollapsibleTrigger asChild>
                  <Button
                    variant="ghost"
                    className="w-full p-6 justify-between text-left hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-xl"
                  >
                    <span className="text-lg font-semibold">Analysis Explanation</span>
                    <ChevronDown className={`h-5 w-5 transition-transform ${isExplanationOpen ? 'rotate-180' : ''}`} />
                  </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="px-6 pb-6">
                  <div className="prose dark:prose-invert max-w-none">
                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                      {data.explanation}
                    </p>
                    <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        Powered by Claude 4
                      </p>
                    </div>
                  </div>
                </CollapsibleContent>
              </Collapsible>
            </Card>
          </div>
        )}

        {Error && (
          <div className="text-center py-12">
            <div className="text-red-500 text-lg mb-4">
              Unable to fetch company data
            </div>
            <p className="text-gray-500 dark:text-gray-400">
              Please try again or check the company name
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 border-t border-gray-200 dark:border-gray-700 bg-white/50 dark:bg-gray-900/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">Powered by</p>
            <div className="flex flex-wrap justify-center items-center gap-6 opacity-60">
              <span className="text-sm font-medium">Anthropic</span>
              <span className="text-sm font-medium">Google</span>
              <span className="text-sm font-medium">Groq</span>
              <span className="text-sm font-medium">Fetch AI</span>
              <span className="text-sm font-medium">Vapi</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
