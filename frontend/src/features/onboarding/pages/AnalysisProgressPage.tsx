import { useEffect, useState, useRef } from 'react';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { Card } from '../../../components/ui/Card';
import { runDatasetAnalysis } from '../../../services/analysis';
import type { AnalysisResultResponse } from '../../../services/analysis';
import { Check, Sparkles, AlertCircle } from 'lucide-react';

interface ProgressStep {
  label: string;
  state: 'pending' | 'active' | 'completed';
}

export default function AnalysisProgressPage() {
  const { uploadState, completeAnalysis } = useWorkspace();
  const [steps, setSteps] = useState<ProgressStep[]>([
    { label: 'Understanding Dataset...', state: 'active' },
    { label: 'Detecting Domain...', state: 'pending' },
    { label: 'Understanding Entity...', state: 'pending' },
    { label: 'Selecting Dashboard...', state: 'pending' },
    { label: 'Preparing Insights...', state: 'pending' },
    { label: 'Selecting Charts...', state: 'pending' },
    { label: 'Generating Recommendations...', state: 'pending' },
    { label: 'Finalizing Workspace...', state: 'pending' },
  ]);

  const [progressPercent, setProgressPercent] = useState(0);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResultResponse | null>(null);
  const hasTriggered = useRef(false);

  useEffect(() => {
    if (!uploadState?.datasetId || hasTriggered.current) return;
    hasTriggered.current = true;

    const triggerBackendAnalysis = async () => {
      try {
        const datasetIdNum = parseInt(uploadState.datasetId, 10);
        const result = await runDatasetAnalysis(datasetIdNum);
        setAnalysisResult(result);
      } catch (err: any) {
        console.error("Backend analysis failed:", err);
        setAnalysisError(err.message || "Failed to calculate business metrics on the backend.");
      }
    };
    triggerBackendAnalysis();
  }, [uploadState?.datasetId]);

  useEffect(() => {
    let currentStepIndex = 0;
    
    const interval = setInterval(() => {
      if (currentStepIndex >= steps.length) {
        clearInterval(interval);
        
        // Retrieve actual database values populated during ingestion
        const datasetType = analysisResult?.semantic_profile?.domain || uploadState?.datasetType || 'Standard Dataset';
        const rowsCount = uploadState?.rowsCount || 0;
        const colsCount = uploadState?.colsCount || 0;
        const businessPulse = Math.round(uploadState?.qualityScore || 95);
        const topInsight = analysisResult?.semantic_profile?.understanding_reasoning || `Successfully loaded ${rowsCount} rows.`;
        
        const emoji = analysisResult?.semantic_profile?.suggested_icon || '💼';
        const rawName = analysisResult?.semantic_profile?.suggested_workspace_name || 'Business Analysis';
        const suggestedWorkspaceName = `${emoji} ${rawName}`;

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

      setSteps((prevSteps: ProgressStep[]) => {
        const nextSteps = prevSteps.map((step: ProgressStep, idx: number) => {
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
  }, [uploadState, completeAnalysis, steps.length]);

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

        {analysisError && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl text-sm flex items-start gap-2">
            <AlertCircle size={16} className="mt-0.5 shrink-0" />
            <p className="m-0 font-medium">{analysisError}</p>
          </div>
        )}

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
          {steps.map((step: ProgressStep, idx: number) => {
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
