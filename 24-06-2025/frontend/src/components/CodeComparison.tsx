'use client';
import { useState } from 'react';

interface CodeData {
  html?: string;
  css?: string;
  js?: string;
}

interface CodeComparisonProps {
  original: CodeData;
  fixed: CodeData;
}

export default function CodeComparison({ original, fixed }: CodeComparisonProps) {
  const [activeTab, setActiveTab] = useState<'html' | 'css' | 'js'>('html');

  const tabs = [
    { id: 'html', label: 'HTML', icon: '🌐' },
    { id: 'css', label: 'CSS', icon: '🎨' },
    { id: 'js', label: 'JavaScript', icon: '⚡' }
  ];

  const renderCodeBlock = (code: string | undefined, type: string, isOriginal: boolean) => {
    if (!code) {
      return (
        <div className="text-gray-500 dark:text-gray-400 text-sm italic p-4">
          No {type.toUpperCase()} code provided
        </div>
      );
    }

    return (
      <pre className="code-block text-xs leading-relaxed overflow-x-auto">
        <code>{code}</code>
      </pre>
    );
  };

  const hasChanges = (type: string) => {
    const originalCode = original[type as keyof CodeData];
    const fixedCode = fixed[type as keyof CodeData];
    return originalCode !== fixedCode && (originalCode || fixedCode);
  };

  return (
    <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
      {/* Header */}
      <div className="bg-slate-50 dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 p-4">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-3 flex items-center gap-2">
          <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Code Comparison
        </h3>
        
        {/* Tab Navigation */}
        <div className="flex space-x-1">
          {tabs.map((tab) => {
            const hasChangesInTab = hasChanges(tab.id);
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as 'html' | 'css' | 'js')}
                className={`
                  flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200
                  ${activeTab === tab.id
                    ? 'bg-blue-500 text-white shadow-md'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-700'
                  }
                  ${hasChangesInTab ? 'ring-2 ring-green-500/50' : ''}
                `}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
                {hasChangesInTab && (
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Code Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-0">
        {/* Original Code */}
        <div className="border-r border-slate-200 dark:border-slate-700">
          <div className="bg-red-50 dark:bg-red-900/20 border-b border-red-200 dark:border-red-800 p-3">
            <h4 className="text-sm font-semibold text-red-700 dark:text-red-300 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              Original Code
            </h4>
          </div>
          <div className="diff-removed">
            {renderCodeBlock(
              original[activeTab as keyof CodeData] as string,
              activeTab,
              true
            )}
          </div>
        </div>

        {/* Fixed Code */}
        <div>
          <div className="bg-green-50 dark:bg-green-900/20 border-b border-green-200 dark:border-green-800 p-3">
            <h4 className="text-sm font-semibold text-green-700 dark:text-green-300 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Fixed Code
            </h4>
          </div>
          <div className="diff-added">
            {renderCodeBlock(
              fixed[activeTab as keyof CodeData] as string,
              activeTab,
              false
            )}
          </div>
        </div>
      </div>

      {/* Summary */}
      <div className="bg-slate-50 dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700 p-4">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-red-500 rounded"></div>
              <span className="text-slate-600 dark:text-slate-400">Original</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-500 rounded"></div>
              <span className="text-slate-600 dark:text-slate-400">Fixed</span>
            </div>
          </div>
          
          <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>
              {hasChanges(activeTab) ? 'Changes detected' : 'No changes'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
} 