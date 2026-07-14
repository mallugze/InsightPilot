import { useWorkspace } from '../../../context/WorkspaceContext';
import { Card } from '../../../components/ui/Card';
import { FolderOpen } from 'lucide-react';

export default function WorkspacesPage() {
  const { workspaceName, profile } = useWorkspace();

  return (
    <div className="space-y-6 max-w-4xl mx-auto pt-8 text-left">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 m-0">Workspace Details</h1>
        <p className="text-slate-500 mt-1">Manage active company datasets and operations.</p>
      </div>

      <Card className="bg-white rounded-xl p-8 border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-secondary/10 text-secondary flex items-center justify-center">
            <FolderOpen size={20} />
          </div>
          <div>
            <h3 className="font-semibold text-slate-800 text-lg m-0">
              {workspaceName || 'Unassigned Workspace'}
            </h3>
            <p className="text-sm text-slate-500 m-0 mt-0.5">
              Personalized workspace active inside browser session.
            </p>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-100 grid grid-cols-2 gap-4 text-sm text-slate-600">
          <div>
            <span className="text-xs text-slate-400 block uppercase font-bold tracking-wider">Owner Profile</span>
            <span className="font-medium text-slate-800">{profile?.fullName || 'Anonymous User'}</span>
          </div>
          <div>
            <span className="text-xs text-slate-400 block uppercase font-bold tracking-wider">Company</span>
            <span className="font-medium text-slate-800">{profile?.companyName || 'Not specified'}</span>
          </div>
        </div>
      </Card>
    </div>
  );
}
