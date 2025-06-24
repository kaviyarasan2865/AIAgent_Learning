'use client';
import { useState } from 'react';
import CodeUpload from '../components/CodeUpload';
import IssueReport from '../components/IssueReport';
import FixPreview from '../components/FixPreview';
import ApprovalDashboard from '../components/ApprovalDashboard';
import AuditLog from '../components/AuditLog';

export default function Home() {
  const [submissionId, setSubmissionId] = useState<string | null>(null);
  const [issues, setIssues] = useState<any[]>([]);
  const [fixes, setFixes] = useState<any[]>([]);
  const [dashboard, setDashboard] = useState<any>(null);
  const [auditLog, setAuditLog] = useState<any[]>([]);
  const [approvalMessage, setApprovalMessage] = useState<string | null>(null);
  const [resultData, setResultData] = useState<any>(null);
  const [approved, setApproved] = useState<boolean | null>(null);

  async function handleAnalyze(data: any) {
    setApproved(null);
    const res = await fetch('http://127.0.0.1:8000/api/bug-fix', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input_data: data })
    });
    if (!res.ok) {
      alert('Failed to analyze code.');
      return;
    }
    const result = await res.json();
    setResultData(result.result);
    if (result.result?.status === 'pending' && result.result?.message) {
      setApprovalMessage(result.result.message);
      setFixes(Array.isArray(result.result.fixes) ? result.result.fixes : []);
      setIssues(Array.isArray(result.result.issues) ? result.result.issues : []);
      setDashboard(typeof result.result.dashboard === 'object' ? result.result.dashboard : null);
      setSubmissionId(result.result?.submission_id || null);
      return;
    }
    setApprovalMessage(null);
    setFixes(Array.isArray(result.result?.dashboard?.diff_views) ? result.result.dashboard.diff_views : []);
    setIssues(Array.isArray(result.result?.issues) ? result.result.issues : []);
    setDashboard(typeof result.result?.dashboard === 'object' ? result.result.dashboard : null);
    setSubmissionId(result.result?.submission_id || null);
  }

  function handleApproveClick() {
    setApproved(true);
  }
  function handleRejectClick() {
    setApproved(false);
  }

  return (
    <main className="max-w-4xl mx-auto p-6 bg-card rounded-lg shadow-lg mt-8">
      <h1 className="text-3xl font-extrabold text-primary mb-6">Agentic AI Bug Fixer</h1>
      <CodeUpload onSubmit={handleAnalyze} />

      {/* Show all backend response fields */}
      {resultData && (
        <div className="my-4 p-4 bg-gray-50 border-l-4 border-blue-400 rounded text-gray-800">
          <div className="mb-2 font-bold">Backend Response Summary:</div>
          <div><b>Status:</b> {resultData.status}</div>
          <div><b>Message:</b> {resultData.message}</div>
          <div><b>Dashboard:</b> {typeof resultData.dashboard === 'string' ? resultData.dashboard : JSON.stringify(resultData.dashboard)}</div>
          <div><b>Issues:</b> {typeof resultData.issues === 'string' ? resultData.issues : JSON.stringify(resultData.issues)}</div>
          <div><b>Fixes:</b> {typeof resultData.fixes === 'string' ? resultData.fixes : JSON.stringify(resultData.fixes)}</div>
          <div><b>Optimizations:</b> {typeof resultData.optimizations === 'string' ? resultData.optimizations : JSON.stringify(resultData.optimizations)}</div>
          <div><b>Submission ID:</b> {resultData.submission_id}</div>
        </div>
      )}

      {/* Approval UI */}
      {resultData?.status === 'pending' && (
        <div className="flex gap-4 my-4">
          <button
            className="px-6 py-2 bg-green-500 text-white rounded font-bold hover:bg-green-600"
            onClick={handleApproveClick}
          >
            Approve
          </button>
          <button
            className="px-6 py-2 bg-red-500 text-white rounded font-bold hover:bg-red-600"
            onClick={handleRejectClick}
          >
            Reject
          </button>
        </div>
      )}

      {/* Show optimized code or summary if approved */}
      {approved && resultData && (
        <div className="my-6 p-4 bg-green-50 border-l-4 border-green-500 rounded">
          <div className="font-bold mb-2">Optimized Code / Summary:</div>
          <pre className="bg-white p-3 rounded border border-green-200 overflow-x-auto">
            {typeof resultData.optimizations === 'string'
              ? resultData.optimizations
              : JSON.stringify(resultData.optimizations, null, 2)}
          </pre>
        </div>
      )}

      {/* Show rejection message */}
      {approved === false && (
        <div className="my-6 p-4 bg-red-50 border-l-4 border-red-500 rounded font-bold text-red-700">
          Changes were rejected.
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <IssueReport issues={issues} />
        <FixPreview diffs={fixes} />
      </div>
      <ApprovalDashboard dashboard={dashboard} onApprove={() => {}} />
      <AuditLog logs={auditLog} />
    </main>
  );
}