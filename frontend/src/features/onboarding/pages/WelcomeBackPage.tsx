import { useWorkspace } from '../../../context/WorkspaceContext';
import { Button } from '../../../components/ui/Button';
import { Card } from '../../../components/ui/Card';
import { LogIn, Plus } from 'lucide-react';

export default function WelcomeBackPage() {
  const { profile, workspaceName, setSessionResumed, resetOnboardingKeepProfile } = useWorkspace();

  const handleResume = () => {
    setSessionResumed(true);
  };

  const handleNewWorkspace = () => {
    resetOnboardingKeepProfile();
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center items-center px-4 antialiased selection:bg-secondary-fixed selection:text-on-secondary-fixed">
      <Card className="w-full max-w-md bg-white border border-outline-variant rounded-2xl p-8 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)] flex flex-col text-left">
        {/* Header Icon */}
        <div className="flex items-center gap-2 mb-6">
          <div className="w-8 h-8 rounded bg-primary text-white flex items-center justify-center font-bold text-sm shrink-0">
            IP
          </div>
          <span className="font-display text-xl font-bold tracking-tighter text-primary">InsightPilot</span>
        </div>

        {/* Title Group */}
        <div className="space-y-2 mb-8">
          <h1 className="font-display text-2xl font-bold text-primary m-0 tracking-tight">
            Welcome back, {profile?.fullName || 'User'} 👋
          </h1>
          <p className="font-sans text-sm text-on-surface-variant leading-relaxed m-0">
            Please choose whether you want to resume working in your current workspace or start fresh with a new analysis.
          </p>
        </div>

        {/* Workspace Resumption Preview */}
        <Card className="p-4 bg-slate-50 border border-outline-variant/60 rounded-xl flex flex-col justify-between mb-8">
          <span className="font-label-caps text-[10px] text-on-surface-variant mb-1 uppercase tracking-wider font-semibold">
            Active Workspace
          </span>
          <span className="font-display text-base font-bold text-primary">
            {workspaceName || 'Unassigned Workspace'}
          </span>
        </Card>

        {/* Resumption actions */}
        <div className="flex flex-col gap-3">
          <Button
            onClick={handleResume}
            className="w-full bg-primary text-on-primary py-3 rounded-lg font-label-md text-label-md font-semibold hover:bg-inverse-surface transition-all flex items-center justify-center gap-2 cursor-pointer"
          >
            <LogIn size={16} />
            Resume
          </Button>

          <Button
            onClick={handleNewWorkspace}
            className="w-full bg-transparent border border-outline-variant text-primary py-3 rounded-lg font-label-md text-label-md font-semibold hover:bg-slate-50 transition-all flex items-center justify-center gap-2 cursor-pointer"
          >
            <Plus size={16} />
            Create New Workspace
          </Button>
        </div>
      </Card>
    </div>
  );
}
