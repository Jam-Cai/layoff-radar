import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Search, Shield, Zap, Database, Waves, SmilePlus, User, Users, UserCheck, UserCog, Bot } from 'lucide-react';
import { SiPython, SiReact, SiFastapi, SiTailwindcss, SiTypescript } from "react-icons/si";
import { useTypingAnimation } from '@/hooks/use-typing-animation';

const rotatingTexts = [
  'proactive career decisions',
  'data-driven insights',
  'workforce trend analysis',
];

const Landing = () => {
  const animatedText = useTypingAnimation({
    texts: rotatingTexts,
    typingSpeed: 75,
    deletingSpeed: 35,
    pauseDuration: 1500,
  });

  return (
    <div className="min-h-screen bg-slate-50 relative overflow-hidden">
      {/* Wavy background */}
      <div className="absolute top-0 left-0 w-full h-full z-0">
        <div className="absolute -top-1/4 -left-1/4 w-1/2 h-1/2 bg-rose-300/50 rounded-full filter blur-3xl opacity-50 animate-blob"></div>
        <div className="absolute -bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-purple-300/50 rounded-full filter blur-3xl opacity-50 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-1/4 -left-1/4 w-1/3 h-1/3 bg-violet-400/50 rounded-full filter blur-3xl opacity-50 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10">
        {/* Header */}
        <header className="border-b border-gray-200 bg-white/80 backdrop-blur-md sticky top-0">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
            <div className="flex items-center justify-between">
              <Link to="/" className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">Fs</span>
                </div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  Farsight.fyi
                </h1>
              </Link>
              <div className="flex items-center space-x-4">
                <Link to="/">
                  <Button variant="ghost" size="sm">Home</Button>
                </Link>
                <Link to="/dashboard">
                  <Button className="bg-indigo-600 hover:bg-indigo-700" size="sm">
                    Dashboard
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="text-center lg:text-left">
                <h1 className="text-5xl md:text-7xl font-bold mb-4">
                  <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                    Farsight.fyi
                  </span>
                </h1>
                
                <div className="inline-flex items-center px-4 py-2 rounded-full bg-white shadow-md text-lg text-gray-700 mb-10 h-10">
                  Welcome to&nbsp;
                  <span className="font-semibold text-purple-600">
                    {animatedText}
                    <span className="animate-ping">|</span>
                  </span>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6 lg:gap-8">
                <Card className="p-6 border-0 shadow-lg hover:shadow-xl transition-shadow bg-white/60 backdrop-blur-md">
                  <div className="w-12 h-12 bg-indigo-200/50 rounded-lg flex items-center justify-center mb-4">
                    <Shield className="w-6 h-6 text-indigo-600" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">What is Farsight.fyi?</h3>
                  <p className="text-gray-600">
                    A tool that helps you stay ahead of workforce changes with AI-powered risk analysis. Get real-time insights into potential company restructuring.
                  </p>
                </Card>
                
                <Card className="p-6 border-0 shadow-lg hover:shadow-xl transition-shadow bg-white/60 backdrop-blur-md">
                  <div className="w-12 h-12 bg-rose-200/50 rounded-lg flex items-center justify-center mb-4">
                    <Zap className="w-6 h-6 text-rose-600" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">Why Farsight.fyi?</h3>
                  <p className="text-gray-600">
                    Our advanced AI system analyzes multiple data points, including financial reports, news articles, and market trends to provide accurate risk assessments.
                  </p>
                </Card>

                <Card className="p-6 border-0 shadow-lg hover:shadow-xl transition-shadow bg-rose-200/50 backdrop-blur-md">
                  <div className="w-12 h-12 bg-rose-200/50 rounded-lg flex items-center justify-center mb-4">
                    <Waves className="w-6 h-6 text-rose-600" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">How was Farsight.fyi built?</h3>
                  <div className="flex items-center space-x-4 text-gray-700">
                    <SiPython size={24} title="Python" />
                    <SiFastapi size={24} title="FastAPI" />
                    <SiReact size={24} title="React" />
                    <SiTypescript size={24} title="TypeScript" />
                    <SiTailwindcss size={24} title="Tailwind CSS" />
                    <Bot size={24} className="text-purple-600" />
                  </div>
                </Card>
                
                <Card className="p-6 border-0 shadow-lg hover:shadow-xl transition-shadow bg-purple-200/50 backdrop-blur-md">
                  <div className="w-12 h-12 bg-purple-200/50 rounded-lg flex items-center justify-center mb-4">
                    <SmilePlus className="w-6 h-6 text-purple-600" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">Developed and Designed by</h3>
                  <div className="flex flex-wrap gap-3 justify-center">
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white shadow-md hover:shadow-lg transition-shadow cursor-pointer">
                      <User className="w-8 h-8" />
                    </div>
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white shadow-md hover:shadow-lg transition-shadow cursor-pointer">
                      <Users className="w-8 h-8" />
                    </div>
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center text-white shadow-md hover:shadow-lg transition-shadow cursor-pointer">
                      <UserCheck className="w-8 h-8" />
                    </div>
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-orange-400 to-orange-600 flex items-center justify-center text-white shadow-md hover:shadow-lg transition-shadow cursor-pointer">
                      <UserCog className="w-8 h-8" />
                    </div>
                  </div>
                </Card>
              </div>
            </div>

            <div className="lg:col-span-1 flex items-center">
              <Card className="p-6 border-0 shadow-2xl w-full bg-gradient-to-br from-purple-600 to-indigo-700 text-white transform transition-all duration-300 hover:scale-105 translate-y-8">
                <h3 className="text-2xl font-bold mb-4">Try It Out</h3>
                <p className="text-indigo-200 mb-8">
                  Get real-time insights into potential company restructuring. Analyze any company's layoff risk now.
                </p>
                <Link to="/dashboard">
                  <Button size="lg" className="w-full bg-white text-indigo-600 hover:bg-gray-100 text-lg font-bold">
                    <Search className="w-5 h-5 mr-2" />
                    Analyze Company Risk
                  </Button>
                </Link>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Landing; 