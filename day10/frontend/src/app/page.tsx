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

  async function handleAnalyze(data: any) {
    // Call the Next.js API route that proxies to FastAPI
    const res = await fetch('/api/bug-fix', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input_data: data })
    });
    const result = await res.json();
    // You can update state with result.result or handle errors
    setFixes(result.result);
    // Optionally set issues, dashboard, etc. from result
  }

  async function handleApproval(approved: boolean) {
    if (!submissionId) return;
    const res = await fetch('/api/approval', { method: 'POST', body: JSON.stringify({ codeSubmissionId: submissionId, approved, user: 'user1' }) });
    const approval = await res.json();
    setAuditLog(logs => [...logs, approval]);
    setDashboard(null);
  }

  return (
    <main className="max-w-4xl mx-auto p-6 bg-card rounded-lg shadow-lg mt-8">
      <h1 className="text-3xl font-extrabold text-primary mb-6">Agentic AI Bug Fixer</h1>
      <CodeUpload onSubmit={handleAnalyze} />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <IssueReport issues={issues} />
        <FixPreview diffs={fixes} />
      </div>
      <ApprovalDashboard dashboard={dashboard} onApprove={handleApproval} />
      <AuditLog logs={auditLog} />
    </main>
  );
}