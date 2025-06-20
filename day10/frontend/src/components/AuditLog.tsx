export default function AuditLog({ logs }: { logs: any[] }) {
  if (!logs?.length) return null;
  return (
    <div className="my-10 mx-auto max-w-2xl bg-gradient-to-br from-white/80 to-blue-100 dark:from-gray-900/80 dark:to-blue-950 shadow-2xl rounded-3xl p-8 border border-blue-200 dark:border-blue-900 backdrop-blur-lg">
      <h2 className="font-extrabold text-2xl text-blue-800 dark:text-blue-300 mb-6 flex items-center gap-2">
        <svg width='28' height='28' fill='none' viewBox='0 0 24 24'><rect width='24' height='24' rx='6' fill='#3b82f6' opacity='0.12'/><path d='M6 12h12M12 6v12' stroke='#2563eb' strokeWidth='2' strokeLinecap='round'/></svg>
        Audit Log
      </h2>
      <ul className="space-y-4">
        {logs.map((log, idx) => (
          <li key={idx} className="bg-white/80 dark:bg-gray-900/70 border border-blue-100 dark:border-blue-800 rounded-xl p-4 shadow-md flex items-start gap-3 hover:shadow-xl transition-shadow duration-200">
            <span className="inline-block mt-1">
              <svg width='18' height='18' fill='none' viewBox='0 0 24 24'><circle cx='12' cy='12' r='10' fill='#2563eb' opacity='0.15'/><path d='M8 12l2 2 4-4' stroke='#2563eb' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round'/></svg>
            </span>
            <span className="text-xs font-mono text-gray-700 dark:text-gray-200 break-all">{JSON.stringify(log)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}