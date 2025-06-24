'use client';
import { useState } from 'react';

export default function CodeUpload({ onSubmit }: { onSubmit: (data: any) => void }) {
  const [html, setHtml] = useState('');
  const [css, setCss] = useState('');
  const [js, setJs] = useState('');

  const handleAnalyze = (e: React.FormEvent) => {
    e.preventDefault();
    // Only call the parent onSubmit with the code data, do not call the API here
    if (typeof onSubmit === 'function') onSubmit({ html, css, javascript: js });
  };

  return (
    <form
      
      className="space-y-6 max-w-2xl mx-auto bg-gradient-to-br from-white/80 to-blue-100 dark:from-gray-900/80 dark:to-blue-950 shadow-2xl rounded-3xl p-8 border border-blue-200 dark:border-blue-900 backdrop-blur-lg mt-10"
    >
      <h2 className="text-2xl font-extrabold text-blue-800 dark:text-blue-300 mb-4 flex items-center gap-2">
        <svg width='28' height='28' fill='none' viewBox='0 0 24 24'><rect width='24' height='24' rx='6' fill='#3b82f6' opacity='0.12'/><path d='M8 12h8M12 8v8' stroke='#2563eb' strokeWidth='2' strokeLinecap='round'/></svg>
        Upload Your Code
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label className="block text-sm font-semibold text-blue-700 dark:text-blue-200 mb-2">HTML</label>
          <textarea placeholder="Paste HTML" value={html} onChange={e => setHtml(e.target.value)}
            className="w-full h-32 p-3 border border-blue-200 dark:border-blue-700 rounded-xl bg-white/70 dark:bg-gray-900/70 shadow-inner focus:ring-2 focus:ring-blue-400 transition-all font-mono text-sm resize-none" />
        </div>
        <div>
          <label className="block text-sm font-semibold text-blue-700 dark:text-blue-200 mb-2">CSS</label>
          <textarea placeholder="Paste CSS" value={css} onChange={e => setCss(e.target.value)}
            className="w-full h-32 p-3 border border-emerald-200 dark:border-emerald-700 rounded-xl bg-white/70 dark:bg-gray-900/70 shadow-inner focus:ring-2 focus:ring-emerald-400 transition-all font-mono text-sm resize-none" />
        </div>
        <div>
          <label className="block text-sm font-semibold text-blue-700 dark:text-blue-200 mb-2">JavaScript</label>
          <textarea placeholder="Paste JavaScript" value={js} onChange={e => setJs(e.target.value)}
            className="w-full h-32 p-3 border border-yellow-200 dark:border-yellow-700 rounded-xl bg-white/70 dark:bg-gray-900/70 shadow-inner focus:ring-2 focus:ring-yellow-400 transition-all font-mono text-sm resize-none" />
        </div>
      </div>
      <div className="flex justify-end mt-6">
        <button onClick={handleAnalyze} className="px-8 py-3 bg-gradient-to-r from-blue-500 to-emerald-500 hover:from-blue-600 hover:to-emerald-600 text-white font-bold rounded-2xl shadow-lg transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg flex items-center gap-2">
          <svg width='22' height='22' fill='none' viewBox='0 0 24 24'><circle cx='12' cy='12' r='10' fill='#2563eb' opacity='0.15'/><path d='M8 12l2 2 4-4' stroke='#fff' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round'/></svg>
          Analyze
        </button>
      </div>
    </form>
  );
}