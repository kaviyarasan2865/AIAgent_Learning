export default function FixPreview({ diffs, fixes }: { diffs?: any[], fixes?: any[] }) {
  const data = Array.isArray(diffs) ? diffs : Array.isArray(fixes) ? fixes : [];
  
  if (!data.length) return null;
  
  return (
    <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg rounded-xl border border-slate-200 dark:border-slate-700 p-6">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12h10M12 7v10" />
        </svg>
        Fix Suggestions
      </h2>
      
      <div className="space-y-4">
        {data.map((fix, idx) => (
          <div
            key={idx}
            className="border border-slate-200 dark:border-slate-700 rounded-lg overflow-hidden bg-slate-50 dark:bg-slate-800"
          >
            {/* Fix Header */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border-b border-blue-200 dark:border-blue-800 p-3">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-blue-800 dark:text-blue-200 text-sm">
                  {fix.type || `Fix ${idx + 1}`}
                </h3>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-xs text-green-600 dark:text-green-400">Auto-generated</span>
                </div>
              </div>
            </div>

            {/* Before/After Comparison */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-0">
              <div className="border-r border-slate-200 dark:border-slate-700">
                <div className="bg-red-50 dark:bg-red-900/20 p-2 border-b border-red-200 dark:border-red-800">
                  <span className="text-xs font-medium text-red-700 dark:text-red-300">Before</span>
                </div>
                <pre className="p-3 text-xs font-mono text-slate-700 dark:text-slate-300 overflow-x-auto diff-removed">
                  {fix.before || 'No changes needed'}
                </pre>
              </div>
              
              <div>
                <div className="bg-green-50 dark:bg-green-900/20 p-2 border-b border-green-200 dark:border-green-800">
                  <span className="text-xs font-medium text-green-700 dark:text-green-300">After</span>
                </div>
                <pre className="p-3 text-xs font-mono text-slate-700 dark:text-slate-300 overflow-x-auto diff-added">
                  {fix.after || 'No changes needed'}
                </pre>
              </div>
            </div>

            {/* Explanation */}
            {fix.explanation && (
              <div className="p-3 bg-slate-100 dark:bg-slate-700 border-t border-slate-200 dark:border-slate-600">
                <p className="text-sm text-slate-600 dark:text-slate-400 italic">
                  {fix.explanation}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}