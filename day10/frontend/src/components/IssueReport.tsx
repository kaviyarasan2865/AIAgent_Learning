export default function IssueReport({ issues }: { issues: any }) {
  if (!issues) return null;
  return (
    <div className="my-10 mx-auto max-w-2xl bg-gradient-to-br from-white/80 to-pink-100 dark:from-gray-900/80 dark:to-pink-950 shadow-2xl rounded-3xl p-8 border border-pink-200 dark:border-pink-900 backdrop-blur-lg">
      <h2 className="font-extrabold text-2xl text-pink-800 dark:text-pink-300 mb-6 flex items-center gap-2">
        <svg width='28' height='28' fill='none' viewBox='0 0 24 24'><rect width='24' height='24' rx='6' fill='#ec4899' opacity='0.12'/><path d='M12 8v4m0 4h.01' stroke='#db2777' strokeWidth='2' strokeLinecap='round'/></svg>
        Detected Issues
      </h2>
      <pre className="bg-gradient-to-br from-pink-50 to-pink-100 dark:from-pink-900 dark:to-pink-950 p-6 rounded-2xl border border-pink-200 dark:border-pink-800 shadow-inner font-mono text-sm text-gray-800 dark:text-pink-100 overflow-x-auto">
        {JSON.stringify(issues, null, 2)}
      </pre>
    </div>
  );
}