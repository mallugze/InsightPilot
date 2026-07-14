import { useEffect, useState } from 'react';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { Card } from '../../../components/ui/Card';
import { Check, Sparkles } from 'lucide-react';

interface ProgressStep {
  label: string;
  state: 'pending' | 'active' | 'completed';
}

export default function AnalysisProgressPage() {
  const { uploadState, completeAnalysis } = useWorkspace();
  const [steps, setSteps] = useState<ProgressStep[]>([
    { label: 'Reading dataset', state: 'active' },
    { label: 'Detecting columns', state: 'pending' },
    { label: 'Identifying dataset type', state: 'pending' },
    { label: 'Finding trends', state: 'pending' },
    { label: 'Detecting anomalies', state: 'pending' },
    { label: 'Preparing executive summary', state: 'pending' },
    { label: 'Building dashboard', state: 'pending' },
  ]);

  const [progressPercent, setProgressPercent] = useState(0);

  useEffect(() => {
    let currentStepIndex = 0;
    
    const interval = setInterval(() => {
      if (currentStepIndex >= steps.length) {
        clearInterval(interval);
        
        // Mock successful analysis completion data
        const datasetType = 'Sales Dataset';
        const rowsCount = 1240;
        const colsCount = 12;
        const businessPulse = 87;
        const topInsight = 'Revenue grew by 14% this quarter, primarily driven by enterprise contract renewals. Mid-market CAC increased by 8%.';
        const suggestedWorkspaceName = 'Q3 Sales Analysis';

        completeAnalysis(
          datasetType,
          rowsCount,
          colsCount,
          businessPulse,
          topInsight,
          suggestedWorkspaceName
        );
        return;
      }

      setSteps((prevSteps) => {
        const nextSteps = prevSteps.map((step, idx) => {
          if (idx < currentStepIndex) {
            return { ...step, state: 'completed' as const };
          } else if (idx === currentStepIndex) {
            return { ...step, state: 'active' as const };
          } else {
            return { ...step, state: 'pending' as const };
          }
        });
        return nextSteps;
      });

      setProgressPercent(Math.round(((currentStepIndex + 1) / steps.length) * 100));
      currentStepIndex++;
    }, 900); // 900ms per step

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center items-center px-4 antialiased selection:bg-secondary-fixed selection:text-on-secondary-fixed">
      <Card className="w-full max-w-md bg-white border border-outline-variant rounded-2xl p-8 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)] flex flex-col text-left">
        {/* Header Icon */}
        <div className="flex items-center gap-2 mb-6">
          <div className="w-8 h-8 rounded bg-primary text-white flex items-center justify-center font-bold text-sm shrink-0">
            <Sparkles size={16} className="animate-spin" style={{ animationDuration: '3s' }} />
          </div>
          <span className="font-display text-xl font-bold tracking-tighter text-primary">InsightPilot AI</span>
        </div>

        {/* Title Block */}
        <div className="space-y-1.5 mb-8">
          <h1 className="font-display text-2xl font-bold text-primary m-0 tracking-tight">
            Analyzing your data...
          </h1>
          <p className="font-sans text-sm text-on-surface-variant leading-relaxed m-0">
            Parsing <span className="font-mono font-semibold text-slate-800">{uploadState?.fileName || 'dataset'}</span>. Please wait.
          </p>
        </div>

        {/* Custom Progress Bar */}
        <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden mb-8 border border-outline-variant/30">
          <div 
            className="h-full bg-secondary transition-all duration-300 ease-out rounded-full"
            style={{ width: `${progressPercent}%` }}
          ></div>
        </div>

        {/* Steps List */}
        <div className="space-y-4">
          {steps.map((step, idx) => {
            const isActive = step.state === 'active';
            const isCompleted = step.state === 'completed';
            
            return (
              <div 
                key={idx} 
                className={`flex items-center gap-4 transition-all duration-200 ${
                  isActive ? 'translate-x-1' : ''
                }`}
              >
                {/* Visual state bulb */}
                <div className={`w-6 h-6 rounded-full flex items-center justify-center border shrink-0 text-xs transition-colors duration-200 ${
                  isCompleted 
                    ? 'bg-emerald-500 text-white border-emerald-500' 
                    : isActive 
                    ? 'bg-secondary/10 border-secondary text-secondary font-bold' 
                    : 'bg-transparent border-outline-variant/60 text-slate-400'
                }`}>
                  {isCompleted ? (
                    <Check size={12} strokeWidth={3} />
                  ) : isActive ? (
                    <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-ping"></span>
                  ) : (
                    <span>{idx + 1}</span>
                  )}
                </div>

                {/* Label text */}
                <span className={`text-sm transition-colors duration-200 ${
                  isCompleted 
                    ? 'text-slate-500 line-through decoration-slate-300' 
                    : isActive 
                    ? 'text-primary font-bold font-display' 
                    : 'text-on-surface-variant'
                }`}>
                  {step.label}
                </span>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
