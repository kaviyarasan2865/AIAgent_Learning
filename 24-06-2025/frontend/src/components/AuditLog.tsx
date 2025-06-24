'use client';
import { useState, useEffect } from 'react';

interface AuditLogProps {
  submissionId?: string;
  logs?: any[];
}

interface LogEntry {
  id: string;
  timestamp: string;
  action: string;
  details: string;
  agent: string;
  status: 'success' | 'warning' | 'error' | 'info';
}

export default function AuditLog({ submissionId, logs }: AuditLogProps) {
  const [auditLogs, setAuditLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (submissionId) {
      fetchAuditLogs();
    } else if (logs) {
      setAuditLogs(Array.isArray(logs) ? logs : []);
    }
  }, [submissionId, logs]);

  const fetchAuditLogs = async () => {
    if (!submissionId) return;
    
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/audit-logs/${submissionId}`);
      if (response.ok) {
        const data = await response.json();
        setAuditLogs(Array.isArray(data.logs) ? data.logs : []);
      }
    } catch (error) {
      console.error('Failed to fetch audit logs:', error);
      setAuditLogs([]);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return (
          <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        );
      case 'warning':
        return (
          <svg className="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        );
      case 'error':
        return (
          <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        );
      default:
        return (
          <svg className="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20';
      case 'warning':
        return 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20';
      case 'error':
        return 'border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20';
      default:
        return 'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20';
    }
  };

  if (!auditLogs.length && !loading) return null;

  return (
    <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg rounded-xl border border-slate-200 dark:border-slate-700 p-6">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        Audit Log
      </h3>

      {loading ? (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          <span className="ml-2 text-slate-600 dark:text-slate-400">Loading audit logs...</span>
        </div>
      ) : (
        <div className="space-y-3">
          {auditLogs.map((log, idx) => (
            <div
              key={log.id || idx}
              className={`p-4 rounded-lg border ${getStatusColor(log.status)} transition-all duration-200 hover:shadow-md`}
            >
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 mt-0.5">
                  {getStatusIcon(log.status)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="text-sm font-semibold text-slate-900 dark:text-white">
                      {log.action || 'Action performed'}
                    </h4>
                    <span className="text-xs text-slate-500 dark:text-slate-400">
                      {log.timestamp ? new Date(log.timestamp).toLocaleTimeString() : 'Just now'}
                    </span>
                  </div>
                  
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                    {log.details || JSON.stringify(log)}
                  </p>
                  
                  {log.agent && (
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-slate-500 dark:text-slate-400">Agent:</span>
                      <span className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30 px-2 py-1 rounded">
                        {log.agent}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))} 
        </div>
      )}
    </div>
  );
}