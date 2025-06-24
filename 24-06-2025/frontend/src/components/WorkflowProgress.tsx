'use client';

type WorkflowStep = 'upload' | 'analyzing' | 'issues' | 'fixes' | 'approval' | 'complete';

interface WorkflowProgressProps {
  currentStep: WorkflowStep;
}

const steps = [
  { id: 'upload', label: 'Upload Code', icon: '📁' },
  { id: 'analyzing', label: 'AI Analysis', icon: '🤖' },
  { id: 'issues', label: 'Issue Detection', icon: '🔍' },
  { id: 'fixes', label: 'Fix Generation', icon: '🔧' },
  { id: 'approval', label: 'User Approval', icon: '✅' },
  { id: 'complete', label: 'Complete', icon: '🎉' }
];

export default function WorkflowProgress({ currentStep }: WorkflowProgressProps) {
  const currentIndex = steps.findIndex(step => step.id === currentStep);

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const isActive = step.id === currentStep;
          const isCompleted = index < currentIndex;
          const isUpcoming = index > currentIndex;

          return (
            <div key={step.id} className="flex items-center">
              {/* Step Circle */}
              <div className="flex flex-col items-center">
                <div
                  className={`
                    w-12 h-12 rounded-full flex items-center justify-center text-lg font-semibold transition-all duration-300
                    ${isCompleted 
                      ? 'bg-green-500 text-white shadow-lg' 
                      : isActive 
                        ? 'bg-blue-500 text-white shadow-lg scale-110' 
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
                    }
                  `}
                >
                  {isCompleted ? '✓' : step.icon}
                </div>
                
                {/* Step Label */}
                <span
                  className={`
                    mt-2 text-xs font-medium text-center max-w-20
                    ${isActive 
                      ? 'text-blue-600 dark:text-blue-400' 
                      : isCompleted 
                        ? 'text-green-600 dark:text-green-400' 
                        : 'text-gray-500 dark:text-gray-400'
                    }
                  `}
                >
                  {step.label}
                </span>
              </div>

              {/* Connector Line */}
              {index < steps.length - 1 && (
                <div className="flex-1 mx-4">
                  <div
                    className={`
                      h-1 rounded-full transition-all duration-300
                      ${isCompleted 
                        ? 'bg-green-500' 
                        : 'bg-gray-200 dark:bg-gray-700'
                      }
                    `}
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Current Step Description */}
      <div className="mt-6 text-center">
        <div className="inline-flex items-center px-4 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-full text-sm font-medium">
          <div className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></div>
          {steps.find(step => step.id === currentStep)?.label}
        </div>
      </div>
    </div>
  );
} 