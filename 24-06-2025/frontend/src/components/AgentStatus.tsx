'use client';

type AgentStatusType = 'idle' | 'processing' | 'completed' | 'error';

interface AgentStatusProps {
  statuses: Record<string, AgentStatusType>;
}

const agents = [
  {
    key: 'layoutValidator',
    name: 'Layout Validator',
    description: 'Detecting layout issues and responsiveness problems',
    icon: '🎨',
    color: 'blue'
  },
  {
    key: 'contentHealer',
    name: 'Content Healer',
    description: 'Identifying broken content and placeholder text',
    icon: '🔧',
    color: 'green'
  },
  {
    key: 'fixGenerator',
    name: 'Fix Generator',
    description: 'Generating intelligent code fixes',
    icon: '⚡',
    color: 'purple'
  },
  {
    key: 'codeOptimizer',
    name: 'Code Optimizer',
    description: 'Applying RAG-based optimizations',
    icon: '🚀',
    color: 'orange'
  },
  {
    key: 'userApproval',
    name: 'User Approval',
    description: 'Preparing approval dashboard',
    icon: '✅',
    color: 'emerald'
  }
];

export default function AgentStatus({ statuses }: AgentStatusProps) {
  const getStatusColor = (status: AgentStatusType, color: string) => {
    switch (status) {
      case 'processing':
        return `bg-${color}-100 dark:bg-${color}-900/30 text-${color}-700 dark:text-${color}-300 border-${color}-200 dark:border-${color}-700`;
      case 'completed':
        return `bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border-green-200 dark:border-green-700`;
      case 'error':
        return `bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 border-red-200 dark:border-red-700`;
      default:
        return `bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700`;
    }
  };

  const getStatusIcon = (status: AgentStatusType) => {
    switch (status) {
      case 'processing':
        return (
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
        );
      case 'completed':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        );
      case 'error':
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        );
      default:
        return (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };

  return (
    <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-lg rounded-xl border border-slate-200 dark:border-slate-700 p-6">
      <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        AI Agent Status
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => {
          const status = statuses[agent.key] || 'idle';
          const isProcessing = status === 'processing';
          
          return (
            <div
              key={agent.key}
              className={`
                p-4 rounded-lg border-2 transition-all duration-300
                ${getStatusColor(status, agent.color)}
                ${isProcessing ? 'agent-status' : ''}
              `}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="text-2xl">{agent.icon}</div>
                  <div>
                    <h4 className="font-semibold text-sm">{agent.name}</h4>
                    <p className="text-xs opacity-75 mt-1">{agent.description}</p>
                  </div>
                </div>
                
                <div className="flex-shrink-0">
                  {getStatusIcon(status)}
                </div>
              </div>
              
              {isProcessing && (
                <div className="mt-3">
                  <div className="w-full bg-current/20 rounded-full h-1">
                    <div className="bg-current h-1 rounded-full animate-pulse" style={{ width: '60%' }}></div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
} 