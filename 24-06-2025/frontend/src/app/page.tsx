'use client';
import { useState, useEffect } from 'react';
import CodeUpload from '../components/CodeUpload';
import WorkflowProgress from '../components/WorkflowProgress';
import IssueReport from '../components/IssueReport';
import FixPreview from '../components/FixPreview';
import ApprovalDashboard from '../components/ApprovalDashboard';
import AuditLog from '../components/AuditLog';
import AgentStatus from '../components/AgentStatus';
import CodeComparison from '../components/CodeComparison';

type WorkflowStep = 'upload' | 'analyzing' | 'issues' | 'fixes' | 'approval' | 'complete';
type AgentStatusType = 'idle' | 'processing' | 'completed' | 'error';

interface AnalysisResult {
  status: string;
  message?: string;
  issues?: any[];
  fixes?: any[];
  optimizations?: any[];
  dashboard?: any;
  submission_id?: string;
  html_fixed?: string;
  css_fixed?: string;
  js_fixed?: string;
  html_original?: string;
  css_original?: string;
  js_original?: string;
}

export default function Home() {
  const [currentStep, setCurrentStep] = useState<WorkflowStep>('upload');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [userDecision, setUserDecision] = useState<'approved' | 'rejected' | null>(null);
  const [agentStatuses, setAgentStatuses] = useState<Record<string, AgentStatusType>>({
    layoutValidator: 'idle',
    contentHealer: 'idle',
    fixGenerator: 'idle',
    codeOptimizer: 'idle',
    userApproval: 'idle'
  });

  const handleAnalyze = async (data: any) => {
    setIsAnalyzing(true);
    setCurrentStep('analyzing');
    setUserDecision(null);
    
    // Simulate agent workflow
    const agents = ['layoutValidator', 'contentHealer', 'fixGenerator', 'codeOptimizer', 'userApproval'];
    
    for (let i = 0; i < agents.length; i++) {
      setAgentStatuses(prev => ({
        ...prev,
        [agents[i]]: 'processing'
      }));
      
      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
      
      setAgentStatuses(prev => ({
        ...prev,
        [agents[i]]: 'completed'
      }));
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/api/bug-fix', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input_data: data })
      });

      if (!res.ok) {
        throw new Error('Failed to analyze code');
      }

      const result = await res.json();
      const analysisData = result.result;
      
      setAnalysisResult(analysisData);
      
      if (analysisData?.status === 'pending') {
        setCurrentStep('approval');
      } else {
        setCurrentStep('issues');
      }
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Failed to analyze code. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleApprove = async () => {
    setUserDecision('approved');
    setCurrentStep('complete');

    if (analysisResult) {
      try {
        await fetch(`/api/approval`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            codeSubmissionId: analysisResult.submission_id,
            approved: true,
            html_fixed: analysisResult.html_fixed,
            css_fixed: analysisResult.css_fixed,
            js_fixed: analysisResult.js_fixed
          })
        });
      } catch (error) {
        console.error('Failed to send approval:', error);
      }
    }
  };

  const handleReject = async () => {
    setUserDecision('rejected');
    setCurrentStep('complete');
    
    if (analysisResult?.submission_id) {
      try {
        await fetch(`http://127.0.0.1:8000/api/approval/${analysisResult.submission_id}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ approved: false })
        });
      } catch (error) {
        console.error('Failed to send rejection:', error);
      }
    }
  };

  const resetWorkflow = () => {
    setCurrentStep('upload');
    setAnalysisResult(null);
    setUserDecision(null);
    setAgentStatuses({
      layoutValidator: 'idle',
      contentHealer: 'idle',
      fixGenerator: 'idle',
      codeOptimizer: 'idle',
      userApproval: 'idle'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg border-b border-slate-200 dark:border-slate-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900 dark:text-white">Agentic AI Bug Fixer</h1>
                <p className="text-sm text-slate-600 dark:text-slate-400">Intelligent Code Analysis & Fix Generation</p>
              </div>
            </div>
            
            {currentStep !== 'upload' && (
              <button
                onClick={resetWorkflow}
                className="px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
              >
                Start New Analysis
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Workflow Progress */}
        <WorkflowProgress currentStep={currentStep} />

        {/* Agent Status Dashboard */}
        {isAnalyzing && (
          <div className="mb-8">
            <AgentStatus statuses={agentStatuses} />
          </div>
        )}

        {/* Main Content */}
        <div className="space-y-8">
          {/* Code Upload Step */}
          {currentStep === 'upload' && (
            <div className="fade-in">
              <CodeUpload onSubmit={handleAnalyze} />
            </div>
          )}

          {/* Analysis in Progress */}
          {isAnalyzing && (
            <div className="text-center py-12">
              <div className="inline-flex items-center px-4 py-2 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 rounded-full">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                Analyzing your code with AI agents...
              </div>
            </div>
          )}

          {/* Results Display */}
          {analysisResult && !isAnalyzing && (
            <div className="space-y-8">
              {/* Issues and Fixes Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <IssueReport issues={analysisResult.issues || []} />
                <FixPreview fixes={analysisResult.fixes || []} />
              </div>

              {/* Code Comparison */}
              {analysisResult.html_fixed || analysisResult.css_fixed || analysisResult.js_fixed ? (
                <CodeComparison
                  original={{
                    html: analysisResult.html_original,
                    css: analysisResult.css_original,
                    js: analysisResult.js_original
                  }}
                  fixed={{
                    html: analysisResult.html_fixed,
                    css: analysisResult.css_fixed,
                    js: analysisResult.js_fixed
                  }}
                />
              ) : null}

              {/* Approval Dashboard */}
              {currentStep === 'approval' && (
                <ApprovalDashboard
                  dashboard={analysisResult.dashboard}
                  onApprove={handleApprove}
                  onReject={handleReject}
                />
              )}

              {/* Completion State */}
              {currentStep === 'complete' && (
                <div className="text-center py-12">
                  {userDecision === 'approved' ? (
                    <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-xl p-8">
                      <div className="w-16 h-16 bg-green-100 dark:bg-green-900/40 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg className="w-8 h-8 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-green-800 dark:text-green-200 mb-2">
                        Changes Approved!
                      </h3>
                      <p className="text-green-600 dark:text-green-400">
                        Your optimized code has been generated and is ready for use.
                      </p>
                    </div>
                  ) : (
                    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-8">
                      <div className="w-16 h-16 bg-red-100 dark:bg-red-900/40 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg className="w-8 h-8 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-red-800 dark:text-red-200 mb-2">
                        Changes Rejected
                      </h3>
                      <p className="text-red-600 dark:text-red-400">
                        No changes were applied. You can start a new analysis if needed.
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Audit Log */}
          {analysisResult && (
            <AuditLog submissionId={analysisResult.submission_id} />
          )}
        </div>
      </main>
    </div>
  );
}