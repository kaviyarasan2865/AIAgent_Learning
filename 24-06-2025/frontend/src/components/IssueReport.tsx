export default function IssueReport({ issues }: { issues: any[] }) {
  // Ensure issues is always an array
  const issuesArray = Array.isArray(issues) ? issues : [];
  
  if (!issuesArray.length) return null;

  const getIssueIcon = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'layout':
      case 'css':
        return '🎨';
      case 'javascript':
      case 'js':
        return '⚡';
      case 'html':
        return '🌐';
      case 'content':
        return '📝';
      case 'accessibility':
        return '♿';
      default:
        return '⚠️';
    }
  };

  const getIssueColor = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'layout':
      case 'css':
        return 'blue';
      case 'javascript':
      case 'js':
        return 'purple';
      case 'html':
        return 'green';
      case 'content':
        return 'amber';
      case 'accessibility':
        return 'emerald';
      default:
        return 'red';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800';
      case 'high':
        return 'bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 border-orange-200 dark:border-orange-800';
      case 'medium':
        return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800';
      case 'low':
        return 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800';
      default:
        return 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    }
  };

  return (
    <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg rounded-xl border border-slate-200 dark:border-slate-700 p-6">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        Detected Issues ({issuesArray.length})
      </h2>
      
      <div className="space-y-3">
        {issuesArray.map((issue, idx) => {
          const issueType = issue.type || issue.category || 'general';
          const severity = issue.severity || issue.priority || 'medium';
          const color = getIssueColor(issueType);
          
          return (
            <div
              key={idx}
              className={`p-4 rounded-lg border ${getSeverityColor(severity)} transition-all duration-200 hover:shadow-md`}
            >
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 text-2xl">
                  {getIssueIcon(issueType)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-sm text-slate-900 dark:text-white">
                      {issue.title || issue.message || `Issue ${idx + 1}`}
                    </h3>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-medium px-2 py-1 rounded-full bg-${color}-100 dark:bg-${color}-900/30 text-${color}-700 dark:text-${color}-300`}>
                        {issueType}
                      </span>
                      <span className={`text-xs font-medium px-2 py-1 rounded-full ${getSeverityColor(severity)}`}>
                        {severity}
                      </span>
                    </div>
                  </div>
                  
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                    {issue.description || issue.details || issue.message}
                  </p>
                  
                  {issue.location && (
                    <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      <span>{issue.location}</span>
                    </div>
                  )}
                  
                  {issue.suggestion && (
                    <div className="mt-2 p-2 bg-slate-100 dark:bg-slate-700 rounded text-xs text-slate-600 dark:text-slate-400">
                      <strong>Suggestion:</strong> {issue.suggestion}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}