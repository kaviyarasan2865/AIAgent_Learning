export default function FixPreview({ diffs }: { diffs: any[] }) {
  if (!diffs?.length) return null;
  return (
    <div className="mb-8">
      <h2 className="font-bold text-2xl text-blue-700 dark:text-blue-300 mb-4 flex items-center gap-2">
        <svg
          width="24"
          height="24"
          fill="none"
          viewBox="0 0 24 24"
          className="shrink-0"
        >
          <rect
            width="24"
            height="24"
            rx="6"
            fill="#3b82f6"
            opacity="0.12"
          />
          <path
            d="M7 12h10M12 7v10"
            stroke="#2563eb"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
        Fix Suggestions (Before/After)
      </h2>
      {diffs.map((diff, idx) => (
        <div
          key={idx}
          className="my-6 p-6 border border-blue-200 dark:border-blue-800 rounded-2xl bg-white/70 dark:bg-gray-900/70 shadow-lg hover:shadow-2xl transition-shadow duration-200"
        >
          <div className="font-semibold text-lg text-blue-800 dark:text-blue-200 mb-2 flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-gradient-to-r from-blue-400 to-blue-600 mr-2"></span>
            {diff.type}
          </div>
          <div className="flex flex-col md:flex-row gap-6">
            <div className="w-full md:w-1/2">
              <div className="text-xs text-gray-500 mb-1">Before</div>
              <pre className="bg-gradient-to-br from-red-100 to-red-200 dark:from-red-900 dark:to-red-800 p-3 rounded-lg text-sm overflow-x-auto border border-red-200 dark:border-red-700 shadow-inner font-mono">
                {diff.before}
              </pre>
            </div>
            <div className="w-full md:w-1/2">
              <div className="text-xs text-gray-500 mb-1">After</div>
              <pre className="bg-gradient-to-br from-green-100 to-emerald-100 dark:from-green-900 dark:to-emerald-900 p-3 rounded-lg text-sm overflow-x-auto border border-green-200 dark:border-green-700 shadow-inner font-mono">
                {diff.after}
              </pre>
            </div>
          </div>
          <div className="text-base mt-4 text-gray-700 dark:text-gray-300 italic border-l-4 border-blue-300 dark:border-blue-700 pl-4 bg-blue-50/60 dark:bg-blue-900/30 py-2">
            {diff.explanation}
          </div>
        </div>
      ))}
    </div>
  );
}