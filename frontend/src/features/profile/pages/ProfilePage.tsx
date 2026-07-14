import { useState } from 'react';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { Card } from '../../../components/ui/Card';
import { getSessionId } from '../../../utils/storage';
import { 
  User, 
  Mail, 
  Building2, 
  FolderHeart, 
  Calendar, 
  Files, 
  BarChart, 
  HardDrive,
  ChevronDown,
  ChevronUp,
  Cpu
} from 'lucide-react';

export default function ProfilePage() {
  const { profile, uploadState, analysisState, workspaceName } = useWorkspace();
  const [showDevInfo, setShowDevInfo] = useState(false);

  // Derive simple metrics from mock state
  const hasUploaded = uploadState ? 1 : 0;
  const hasAnalyses = analysisState === 'completed' ? 1 : 0;
  const storageUsed = uploadState?.fileSize || '0 KB';
  const memberSince = profile?.memberSince || 'July 2026';

  return (
    <div className="space-y-6 max-w-4xl mx-auto pt-8 text-left px-margin-page pb-section-gap">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 m-0">My Profile</h1>
        <p className="text-slate-500 mt-1">Review user accounts, local workspace usage, and technical session details.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Core Account Details Card (Col 1 & 2) */}
        <Card className="md:col-span-2 bg-white rounded-xl p-8 border border-slate-200 shadow-sm space-y-6">
          <h3 className="font-semibold text-slate-800 text-lg m-0 border-b border-slate-100 pb-3">
            Account Information
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-slate-50 rounded-lg text-slate-500">
                <User size={20} />
              </div>
              <div className="flex flex-col">
                <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Full Name</span>
                <span className="font-medium text-slate-800 text-sm mt-0.5">{profile?.fullName || 'Anonymous User'}</span>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-slate-50 rounded-lg text-slate-500">
                <Mail size={20} />
              </div>
              <div className="flex flex-col">
                <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Email Address</span>
                <span className="font-medium text-slate-800 text-sm mt-0.5">{profile?.email || 'N/A'}</span>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-slate-50 rounded-lg text-slate-500">
                <Building2 size={20} />
              </div>
              <div className="flex flex-col">
                <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Company</span>
                <span className="font-medium text-slate-800 text-sm mt-0.5">{profile?.companyName || 'Not Specified'}</span>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-slate-50 rounded-lg text-slate-500">
                <Calendar size={20} />
              </div>
              <div className="flex flex-col">
                <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Member Since</span>
                <span className="font-medium text-slate-800 text-sm mt-0.5">{memberSince}</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Current Active Workspace Summary (Col 3) */}
        <Card className="bg-white rounded-xl p-8 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div className="space-y-4">
            <h3 className="font-semibold text-slate-800 text-lg m-0 border-b border-slate-100 pb-3 flex items-center gap-2">
              <FolderHeart size={18} className="text-secondary" />
              Active Workspace
            </h3>
            <p className="font-display font-bold text-primary text-xl leading-tight m-0">
              {workspaceName || 'No Active Workspace'}
            </p>
          </div>
          <div className="text-xs text-slate-400 mt-6 pt-4 border-t border-slate-50">
            Assigned during initialization session
          </div>
        </Card>
      </div>

      {/* Usage Analytics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <Card className="p-6 bg-white border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center shrink-0">
            <Files size={22} />
          </div>
          <div className="flex flex-col text-left">
            <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Files Uploaded</span>
            <span className="text-2xl font-bold text-slate-800 mt-0.5">{hasUploaded}</span>
          </div>
        </Card>

        <Card className="p-6 bg-white border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 bg-emerald-50 text-emerald-500 rounded-xl flex items-center justify-center shrink-0">
            <BarChart size={22} />
          </div>
          <div className="flex flex-col text-left">
            <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Analyses Completed</span>
            <span className="text-2xl font-bold text-slate-800 mt-0.5">{hasAnalyses}</span>
          </div>
        </Card>

        <Card className="p-6 bg-white border border-slate-200 shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 bg-amber-50 text-amber-500 rounded-xl flex items-center justify-center shrink-0">
            <HardDrive size={22} />
          </div>
          <div className="flex flex-col text-left">
            <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Storage Occupied</span>
            <span className="text-2xl font-bold text-slate-800 mt-0.5">{storageUsed}</span>
          </div>
        </Card>
      </div>

      {/* Collapsible Developer Information */}
      <Card className="bg-white border border-slate-200 shadow-sm overflow-hidden">
        <button 
          onClick={() => setShowDevInfo(!showDevInfo)}
          className="w-full px-8 py-5 flex items-center justify-between font-semibold text-slate-700 bg-slate-50 hover:bg-slate-100 transition-colors border-b border-slate-100 cursor-pointer"
        >
          <span className="flex items-center gap-2">
            <Cpu size={18} />
            Developer Information
          </span>
          {showDevInfo ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </button>

        {showDevInfo && (
          <div className="px-8 py-6 space-y-4 font-mono text-xs text-slate-600 bg-slate-50/50 leading-relaxed">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-2">
              <span className="font-bold text-slate-500 uppercase">Session ID</span>
              <span className="text-slate-800 select-all font-semibold mt-1 sm:mt-0">{getSessionId() || 'N/A'}</span>
            </div>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-2">
              <span className="font-bold text-slate-500 uppercase">Environment</span>
              <span className="text-slate-800 font-semibold mt-1 sm:mt-0">Local Sandbox (MVP Dev)</span>
            </div>
            <div className="flex flex-col border-b border-slate-100 pb-2">
              <span className="font-bold text-slate-500 uppercase mb-1">User Agent</span>
              <span className="text-slate-800 select-all leading-normal">{navigator.userAgent}</span>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}
