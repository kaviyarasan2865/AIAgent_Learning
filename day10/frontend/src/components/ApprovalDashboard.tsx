'use client';
import React from 'react';
import FixPreview from './FixPreview';

export default function ApprovalDashboard({ dashboard, onApprove }: { dashboard: any, onApprove: (approved: boolean) => void }) {
  if (!dashboard) return null;
  return (
    <div className="my-10 mx-auto max-w-3xl bg-gradient-to-br from-white/80 to-blue-100 dark:from-gray-900/80 dark:to-blue-950 shadow-2xl rounded-3xl p-8 border border-blue-200 dark:border-blue-900 backdrop-blur-lg">
      <h2 className="font-extrabold text-3xl text-blue-800 dark:text-blue-300 mb-6 tracking-tight flex items-center gap-2">
        <svg width="32" height="32" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#2563eb" opacity="0.15"/><path d="M8 12l2 2 4-4" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
        Approval Dashboard
      </h2>
      <FixPreview diffs={dashboard.diff_views} />
      <div className="flex gap-4 mt-8 justify-end">
        <button className="px-6 py-2 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold rounded-xl shadow-lg transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-400" onClick={() => onApprove(true)}>
          Approve All
        </button>
        <button className="px-6 py-2 bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white font-semibold rounded-xl shadow-lg transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-red-400" onClick={() => onApprove(false)}>
          Reject All
        </button>
      </div>
    </div>
  );
}