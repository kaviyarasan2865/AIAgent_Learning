'use client';
import React from 'react';
import FixPreview from './FixPreview';

function ManualFixes({ manualFixes }: { manualFixes: any[] }) {
  if (!manualFixes?.length) return null;
  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold text-amber-800 dark:text-amber-200 mb-3 flex items-center gap-2">
        <svg className="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        Manual Fix Required
      </h3>
      <div className="space-y-3">
        {manualFixes.map((fix, idx) => (
          <div key={idx} className="p-4 border border-amber-200 dark:border-amber-700 rounded-lg bg-amber-50 dark:bg-amber-900/20">
            <div className="font-semibold text-sm text-amber-800 dark:text-amber-200 mb-1">
              {fix.issue}
            </div>
            <div className="text-sm text-amber-700 dark:text-amber-300">
              {fix.reason}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

interface ApprovalDashboardProps {
  dashboard: any;
  onApprove: () => void;
  onReject: () => void;
}

export default function ApprovalDashboard({ dashboard, onApprove, onReject }: ApprovalDashboardProps) {
  if (!dashboard) return null;
  
  return (
    <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg rounded-xl border border-slate-200 dark:border-slate-700 p-6">
      <div className="text-center mb-6">
        <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/40 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
          Review Changes
        </h2>
        <p className="text-slate-600 dark:text-slate-400">
          Please review the proposed fixes before applying them to your code
        </p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800">
          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {dashboard.diff_views?.length || 0}
          </div>
          <div className="text-sm text-blue-700 dark:text-blue-300">Auto Fixes</div>
        </div>
        <div className="bg-amber-50 dark:bg-amber-900/20 p-4 rounded-lg border border-amber-200 dark:border-amber-800">
          <div className="text-2xl font-bold text-amber-600 dark:text-amber-400">
            {dashboard.manual_fix_required?.length || 0}
          </div>
          <div className="text-sm text-amber-700 dark:text-amber-300">Manual Fixes</div>
        </div>
        <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800">
          <div className="text-2xl font-bold text-green-600 dark:text-green-400">
            {dashboard.optimizations?.length || 0}
          </div>
          <div className="text-sm text-green-700 dark:text-green-300">Optimizations</div>
        </div>
      </div>

      {/* Fix Preview */}
      <FixPreview diffs={dashboard.diff_views} />
      
      {/* Manual Fixes */}
      <ManualFixes manualFixes={dashboard.manual_fix_required} />

      {/* Approval Actions */}
      <div className="flex flex-col sm:flex-row gap-4 mt-8 pt-6 border-t border-slate-200 dark:border-slate-700">
        <button 
          onClick={onReject}
          className="flex-1 px-6 py-3 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
          Reject Changes
        </button>
        <button 
          onClick={onApprove}
          className="flex-1 px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          Approve Changes
        </button>
      </div>
    </div>
  );
}