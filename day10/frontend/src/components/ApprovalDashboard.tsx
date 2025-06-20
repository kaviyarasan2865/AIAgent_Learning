'use client';
import React from 'react';
import FixPreview from './FixPreview';

function ManualFixes({ manualFixes }: { manualFixes: any[] }) {
  if (!manualFixes?.length) return null;
  return (
    <div className="mb-8">
      <h2 className="font-bold text-2xl text-yellow-700 dark:text-yellow-300 mb-4 flex items-center gap-2">
        <svg width="24" height="24" fill="none" viewBox="0 0 24 24" className="shrink-0">
          <rect width="24" height="24" rx="6" fill="#facc15" opacity="0.12" />
          <path d="M12 8v4m0 4h.01" stroke="#ca8a04" strokeWidth="2" strokeLinecap="round" />
        </svg>
        Manual Fix Required
      </h2>
      {manualFixes.map((fix, idx) => (
        <div key={idx} className="my-4 p-4 border border-yellow-300 dark:border-yellow-700 rounded-xl bg-yellow-50/80 dark:bg-yellow-900/70 shadow-inner">
          <div className="font-semibold text-base text-yellow-800 dark:text-yellow-200 mb-2">
            {fix.issue}
          </div>
          <div className="text-sm text-gray-700 dark:text-gray-300 italic">
            {fix.reason}
          </div>
        </div>
      ))}
    </div>
  );
}

export default function ApprovalDashboard({ dashboard, onApprove }: { dashboard: any, onApprove: (approved: boolean) => void }) {
  if (!dashboard) return null;
  return (
    <div className="my-10 mx-auto max-w-3xl bg-gradient-to-br from-white/80 to-blue-100 dark:from-gray-900/80 dark:to-blue-950 shadow-2xl rounded-3xl p-8 border border-blue-200 dark:border-blue-900 backdrop-blur-lg">
      <h2 className="font-extrabold text-3xl text-blue-800 dark:text-blue-300 mb-6 tracking-tight flex items-center gap-2">
        <svg width="32" height="32" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#2563eb" opacity="0.15"/><path d="M8 12l2 2 4-4" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
        Approval Dashboard
      </h2>
      <FixPreview diffs={dashboard.diff_views} />
      <ManualFixes manualFixes={dashboard.manual_fix_required} />
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