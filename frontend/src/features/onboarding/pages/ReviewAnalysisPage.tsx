import React, { useState } from 'react';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { Button } from '../../../components/ui/Button';
import { Card } from '../../../components/ui/Card';
import { 
  Sparkles, 
  Columns, 
  Rows, 
  Activity, 
  ArrowRight,
  Edit2
} from 'lucide-react';

export default function ReviewAnalysisPage() {
  const { uploadState, workspaceName, confirmWorkspace } = useWorkspace();
  const [workspaceInput, setWorkspaceInput] = useState(workspaceName || 'My Business Workspace');
  const [isEditing, setIsEditing] = useState(false);

  const handleConfirm = (e: React.FormEvent) => {
    e.preventDefault();
    if (!workspaceInput.trim()) return;
    confirmWorkspace(workspaceInput.trim());
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center items-center px-4 py-8 antialiased selection:bg-secondary-fixed selection:text-on-secondary-fixed">
      <Card className="w-full max-w-lg bg-white border border-outline-variant rounded-2xl p-8 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)] flex flex-col text-left">
        {/* Header Branding */}
        <div className="flex items-center gap-2 mb-6">
          <div className="w-8 h-8 rounded bg-primary text-white flex items-center justify-center font-bold text-sm shrink-0">
            IP
          </div>
          <span className="font-display text-xl font-bold tracking-tighter text-primary">InsightPilot Analysis</span>
        </div>

        {/* Title */}
        <div className="space-y-2 mb-6">
          <h1 className="font-display text-2xl font-bold text-primary m-0 tracking-tight">
            Review Analysis
          </h1>
          <p className="font-sans text-sm text-on-surface-variant leading-relaxed m-0">
            InsightPilot successfully structured your dataset. Here is an overview of your file properties and findings.
          </p>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <Card className="p-4 bg-surface rounded-xl border border-outline-variant/60 flex flex-col justify-between">
            <span className="font-label-caps text-label-caps text-on-surface-variant mb-1 uppercase tracking-wider">Dataset Type</span>
            <span className="font-display text-base font-bold text-primary">{uploadState?.datasetType || 'Standard Dataset'}</span>
          </Card>

          <Card className="p-4 bg-surface rounded-xl border border-outline-variant/60 flex flex-col justify-between">
            <span className="font-label-caps text-label-caps text-on-surface-variant mb-1 uppercase tracking-wider">Business Pulse</span>
            <div className="flex items-center gap-1.5 mt-1">
              <Activity className="text-secondary shrink-0" size={16} />
              <span className="font-display text-base font-bold text-primary">{uploadState?.businessPulse || 100}/100</span>
            </div>
          </Card>

          <Card className="p-4 bg-surface rounded-xl border border-outline-variant/60 flex items-center gap-3">
            <div className="p-2 bg-slate-100 rounded-lg text-slate-500">
              <Rows size={16} />
            </div>
            <div className="flex flex-col">
              <span className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wider">Rows</span>
              <span className="font-display text-sm font-bold text-primary">{uploadState?.rowsCount?.toLocaleString() || 0}</span>
            </div>
          </Card>

          <Card className="p-4 bg-surface rounded-xl border border-outline-variant/60 flex items-center gap-3">
            <div className="p-2 bg-slate-100 rounded-lg text-slate-500">
              <Columns size={16} />
            </div>
            <div className="flex flex-col">
              <span className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wider">Columns</span>
              <span className="font-display text-sm font-bold text-primary">{uploadState?.colsCount || 0}</span>
            </div>
          </Card>
        </div>

        {/* Top Insight panel */}
        <div className="bg-[#F0F7FF] border border-outline-variant/60 border-l-[3px] border-l-secondary-container rounded-xl p-5 mb-6 text-left">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="text-secondary-container" size={16} />
            <h4 className="font-display text-xs font-semibold text-primary m-0 uppercase tracking-wider">Primary AI Insight</h4>
          </div>
          <p className="font-body-sm text-sm text-on-surface leading-relaxed m-0">
            {uploadState?.topInsight || 'Reviewing key anomalies.'}
          </p>
        </div>

        {/* Suggest Workspace Section */}
        <form onSubmit={handleConfirm} className="space-y-4">
          <div className="space-y-2">
            <label className="font-display text-xs font-semibold text-on-surface uppercase tracking-wider block">
              WORKSPACE NAME
            </label>
            <div className="relative flex items-center">
              <input
                type="text"
                disabled={!isEditing}
                value={workspaceInput}
                onChange={(e) => setWorkspaceInput(e.target.value)}
                placeholder="e.g. Sales Analysis"
                className={`w-full bg-surface border rounded-lg pl-4 pr-12 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-secondary/10 focus:border-secondary transition-all ${
                  isEditing 
                    ? 'border-secondary bg-white text-primary' 
                    : 'border-outline-variant text-slate-500 bg-slate-50'
                }`}
              />
              <button
                type="button"
                onClick={() => setIsEditing(!isEditing)}
                className="absolute right-3 p-1 text-slate-400 hover:text-secondary transition-colors cursor-pointer"
              >
                <Edit2 size={16} />
              </button>
            </div>
          </div>

          {/* Confirm Button */}
          <Button
            type="submit"
            className="w-full bg-primary text-on-primary py-3 rounded-lg font-label-md text-label-md font-semibold hover:bg-inverse-surface transition-all flex items-center justify-center gap-2 cursor-pointer mt-4"
          >
            Accept & Enter Dashboard
            <ArrowRight size={16} />
          </Button>
        </form>
      </Card>
    </div>
  );
}
