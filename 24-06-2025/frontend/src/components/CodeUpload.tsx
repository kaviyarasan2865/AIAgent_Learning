'use client';
import { useState } from 'react';

export default function CodeUpload({ onSubmit }: { onSubmit: (data: any) => void }) {
  const [html, setHtml] = useState('');
  const [css, setCss] = useState('');
  const [js, setJs] = useState('');

  const handleAnalyze = (e: React.FormEvent) => {
    e.preventDefault();
    if (typeof onSubmit === 'function') onSubmit({ html, css, javascript: js });
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>, type: 'html' | 'css' | 'js') => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target?.result as string;
        switch (type) {
          case 'html':
            setHtml(content);
            break;
          case 'css':
            setCss(content);
            break;
          case 'js':
            setJs(content);
            break;
        }
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg rounded-xl border border-slate-200 dark:border-slate-700 p-6">
      <div className="text-center mb-6">
        <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/40 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
          Upload Your Code
        </h2>
        <p className="text-slate-600 dark:text-slate-400">
          Paste your HTML, CSS, and JavaScript code for AI-powered analysis and fixes
        </p>
      </div>

      <form onSubmit={handleAnalyze} className="space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* HTML Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">
                HTML Code
              </label>
              <input
                type="file"
                accept=".html,.htm"
                onChange={(e) => handleFileUpload(e, 'html')}
                className="text-xs text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-xs file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-blue-900/30 dark:file:text-blue-300"
              />
            </div>
            <textarea
              placeholder="Paste your HTML code here..."
              value={html}
              onChange={e => setHtml(e.target.value)}
              className="w-full h-40 p-3 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 shadow-sm focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all font-mono text-sm resize-none"
            />
          </div>

          {/* CSS Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">
                CSS Code
              </label>
              <input
                type="file"
                accept=".css"
                onChange={(e) => handleFileUpload(e, 'css')}
                className="text-xs text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-xs file:font-medium file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100 dark:file:bg-emerald-900/30 dark:file:text-emerald-300"
              />
            </div>
            <textarea
              placeholder="Paste your CSS code here..."
              value={css}
              onChange={e => setCss(e.target.value)}
              className="w-full h-40 p-3 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 shadow-sm focus:ring-2 focus:ring-emerald-400 focus:border-transparent transition-all font-mono text-sm resize-none"
            />
          </div>

          {/* JavaScript Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">
                JavaScript Code
              </label>
              <input
                type="file"
                accept=".js,.javascript"
                onChange={(e) => handleFileUpload(e, 'js')}
                className="text-xs text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-xs file:font-medium file:bg-amber-50 file:text-amber-700 hover:file:bg-amber-100 dark:file:bg-amber-900/30 dark:file:text-amber-300"
              />
            </div>
            <textarea
              placeholder="Paste your JavaScript code here..."
              value={js}
              onChange={e => setJs(e.target.value)}
              className="w-full h-40 p-3 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 shadow-sm focus:ring-2 focus:ring-amber-400 focus:border-transparent transition-all font-mono text-sm resize-none"
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-center pt-4">
          <button
            type="submit"
            disabled={!html && !css && !js}
            className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-slate-300 disabled:to-slate-400 disabled:cursor-not-allowed text-white font-semibold rounded-lg shadow-lg transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            Analyze with AI Agents
          </button>
        </div>
      </form>
    </div>
  );
}