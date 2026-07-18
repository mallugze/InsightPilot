import { useState } from 'react';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { Card } from '../../../components/ui/Card';
import { Button } from '../../../components/ui/Button';
import { Badge } from '../../../components/ui/Badge';
import { 
  User, 
  Sliders, 
  Bell, 
  Link2, 
  Info, 
  Check,
  Moon,
  Sun
} from 'lucide-react';

export default function SettingsPage() {
  const { profile, saveProfile } = useWorkspace();
  const [activeTab, setActiveTab] = useState<'profile' | 'theme' | 'workspace' | 'analysis' | 'notifications' | 'api' | 'about'>('profile');
  
  // Profile local state
  const [fullName, setFullName] = useState(profile?.fullName || '');
  const [email, setEmail] = useState(profile?.email || '');
  const [company, setCompany] = useState(profile?.companyName || '');
  
  // Custom preferences states
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [sessionTimeout, setSessionTimeout] = useState('30 Minutes');
  const [mlScoring, setMlScoring] = useState(true);
  const [sigThreshold, setSigThreshold] = useState(0.05);
  const [bellNotifs, setBellNotifs] = useState(true);
  const [apiUrl, setApiUrl] = useState('http://localhost:8000/api');
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleProfileSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    saveProfile(fullName, email, company);
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 3000);
  };

  const menuItems = [
    { id: 'profile', name: 'Profile Settings', icon: <User size={18} /> },
    { id: 'theme', name: 'UI Color Theme', icon: <Sun size={18} /> },
    { id: 'workspace', name: 'Workspaces & Session', icon: <Sliders size={18} /> },
    { id: 'analysis', name: 'Analysis Criteria', icon: <Sliders size={18} /> },
    { id: 'notifications', name: 'Notification Triggers', icon: <Bell size={18} /> },
    { id: 'api', name: 'API Configurations', icon: <Link2 size={18} /> },
    { id: 'about', name: 'About Platform', icon: <Info size={18} /> },
  ] as const;

  return (
    <div className="space-y-6 max-w-4xl mx-auto pt-8 text-left px-margin-page pb-section-gap">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 m-0">System Settings</h1>
        <p className="text-slate-500 mt-1">Configure profile coordinates, UI themes, analysis threshold sliders, and notification triggers.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-gutter">
        {/* Left Side menu navigation */}
        <aside className="md:col-span-4 flex flex-col gap-1">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-semibold transition-all cursor-pointer text-left ${
                activeTab === item.id 
                  ? 'bg-slate-900 text-white shadow-sm' 
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              {item.icon}
              {item.name}
            </button>
          ))}
        </aside>

        {/* Right Side Settings detail views */}
        <div className="md:col-span-8">
          <Card className="bg-white rounded-xl border p-8 shadow-sm min-h-[380px] flex flex-col justify-between">
            <div>
              {/* Profile Details Tab */}
              {activeTab === 'profile' && (
                <form onSubmit={handleProfileSubmit} className="space-y-6">
                  <div className="border-b pb-3">
                    <h3 className="text-base font-bold text-slate-800 m-0">Profile Information</h3>
                    <p className="text-xs text-slate-500 m-0">Update account credentials and registered corporate entities.</p>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex flex-col gap-1.5">
                      <label className="text-xs font-bold text-slate-600 uppercase tracking-wider">Full Name</label>
                      <input 
                        type="text" 
                        required
                        className="border border-slate-200 rounded-lg p-2.5 text-sm focus:outline-none focus:border-slate-800"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                      />
                    </div>

                    <div className="flex flex-col gap-1.5">
                      <label className="text-xs font-bold text-slate-600 uppercase tracking-wider">Email Address</label>
                      <input 
                        type="email" 
                        required
                        className="border border-slate-200 rounded-lg p-2.5 text-sm focus:outline-none focus:border-slate-800"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                      />
                    </div>

                    <div className="flex flex-col gap-1.5">
                      <label className="text-xs font-bold text-slate-600 uppercase tracking-wider">Company Name</label>
                      <input 
                        type="text" 
                        className="border border-slate-200 rounded-lg p-2.5 text-sm focus:outline-none focus:border-slate-800"
                        value={company}
                        onChange={(e) => setCompany(e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="flex items-center gap-3 pt-4">
                    <Button type="submit" className="bg-slate-900 hover:bg-slate-800 text-white font-semibold py-2 px-5 rounded-lg text-sm cursor-pointer flex items-center gap-2">
                      Save Changes
                    </Button>
                    {saveSuccess && (
                      <span className="text-emerald-600 text-xs font-bold flex items-center gap-1">
                        <Check size={14} /> Profile details saved successfully!
                      </span>
                    )}
                  </div>
                </form>
              )}

              {/* UI Color Theme Tab */}
              {activeTab === 'theme' && (
                <div className="space-y-6">
                  <div className="border-b pb-3">
                    <h3 className="text-base font-bold text-slate-800 m-0">UI Color Theme</h3>
                    <p className="text-xs text-slate-500 m-0">Customize visual theme modes for your intelligence dashboard.</p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div 
                      onClick={() => setTheme('light')}
                      className={`border rounded-xl p-6 flex flex-col items-center justify-center gap-3 cursor-pointer transition-all ${
                        theme === 'light' ? 'border-slate-800 ring-2 ring-slate-800/10 bg-slate-50/50' : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <Sun size={28} className="text-amber-500" />
                      <span className="text-sm font-bold text-slate-800">Light Theme</span>
                      <Badge className="bg-slate-100 text-slate-700 text-[10px] font-bold">Standard</Badge>
                    </div>

                    <div 
                      onClick={() => setTheme('dark')}
                      className={`border rounded-xl p-6 flex flex-col items-center justify-center gap-3 cursor-pointer transition-all ${
                        theme === 'dark' ? 'border-slate-800 ring-2 ring-slate-800/10 bg-slate-50/50' : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <Moon size={28} className="text-indigo-500" />
                      <span className="text-sm font-bold text-slate-800">Dark Theme</span>
                      <Badge className="bg-slate-100 text-slate-700 text-[10px] font-bold">Experimental</Badge>
                    </div>
                  </div>
                </div>
              )}

              {/* Workspace Preferences Tab */}
              {activeTab === 'workspace' && (
                <div className="space-y-6">
                  <div className="border-b pb-3">
                    <h3 className="text-base font-bold text-slate-800 m-0">Workspaces & Sessions</h3>
                    <p className="text-xs text-slate-500 m-0">Configure data retention limits and workspace thresholds.</p>
                  </div>
                  
                  <div className="space-y-4 pt-4 text-xs font-semibold">
                    <div className="flex flex-col gap-1.5">
                      <label className="text-xs font-bold text-slate-600 uppercase tracking-wider">Session Expiration Limit</label>
                      <select 
                        value={sessionTimeout}
                        onChange={(e) => setSessionTimeout(e.target.value)}
                        className="border border-slate-200 rounded-lg p-2.5 text-sm bg-white focus:outline-none"
                      >
                        <option>10 Minutes</option>
                        <option>30 Minutes</option>
                        <option>2 Hours</option>
                        <option>Never Expire</option>
                      </select>
                    </div>

                    <div className="bg-slate-50 p-4 border rounded-lg text-slate-600 leading-relaxed font-medium">
                      Note: Datasets uploaded inside temporary directories will expire automatically and clear when active sessions end.
                    </div>
                  </div>
                </div>
              )}

              {/* Analysis Preferences Tab */}
              {activeTab === 'analysis' && (
                <div className="space-y-6">
                  <div className="border-b pb-3">
                    <h3 className="text-base font-bold text-slate-800 m-0">Analysis Preferences</h3>
                    <p className="text-xs text-slate-500 m-0">Modify metrics parameters, statistical limits, and classification scores.</p>
                  </div>
                  
                  <div className="space-y-6 pt-4 text-xs font-semibold">
                    <div className="flex items-center justify-between border-b pb-3">
                      <div>
                        <span className="text-slate-800 text-sm font-bold block">Run ML Readiness Estimators</span>
                        <span className="text-slate-500 text-[11px] font-medium leading-tight">Evaluate Classification & Regression viable task vectors on upload.</span>
                      </div>
                      <input 
                        type="checkbox"
                        checked={mlScoring}
                        onChange={(e) => setMlScoring(e.target.checked)}
                        className="w-4 h-4 cursor-pointer accent-slate-900"
                      />
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between items-center text-xs">
                        <span className="text-slate-800 font-bold">Correlation Significance Alpha Threshold</span>
                        <span className="font-mono font-bold bg-slate-100 px-2 py-0.5 rounded text-slate-700">{sigThreshold}</span>
                      </div>
                      <input 
                        type="range" 
                        min="0.01" 
                        max="0.10" 
                        step="0.01"
                        value={sigThreshold}
                        onChange={(e) => setSigThreshold(parseFloat(e.target.value))}
                        className="w-full h-1 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-900"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Notifications Tab */}
              {activeTab === 'notifications' && (
                <div className="space-y-6">
                  <div className="border-b pb-3">
                    <h3 className="text-base font-bold text-slate-800 m-0">Notification Preferences</h3>
                    <p className="text-xs text-slate-500 m-0">Select what system actions trigger bells or alerts.</p>
                  </div>
                  
                  <div className="space-y-4 pt-4 text-xs font-semibold">
                    <div className="flex items-center justify-between border-b pb-3">
                      <div>
                        <span className="text-slate-800 text-sm font-bold block">Dashboard Bell Alerts</span>
                        <span className="text-slate-500 text-[11px] font-medium leading-tight">Show UI alerts when background profiling runs end.</span>
                      </div>
                      <input 
                        type="checkbox"
                        checked={bellNotifs}
                        onChange={(e) => setBellNotifs(e.target.checked)}
                        className="w-4 h-4 cursor-pointer accent-slate-900"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* API Configuration Tab */}
              {activeTab === 'api' && (
                <div className="space-y-6">
                  <div className="border-b pb-3">
                    <h3 className="text-base font-bold text-slate-800 m-0">API Configurations</h3>
                    <p className="text-xs text-slate-500 m-0">Configure backend server endpoints and gateway settings.</p>
                  </div>
                  
                  <div className="space-y-4 pt-4 text-xs font-semibold">
                    <div className="flex flex-col gap-1.5">
                      <label className="text-xs font-bold text-slate-600 uppercase tracking-wider">FastAPI Backend Origin Base URL</label>
                      <input 
                        type="text" 
                        className="border border-slate-200 rounded-lg p-2.5 text-sm focus:outline-none focus:border-slate-800 font-mono"
                        value={apiUrl}
                        onChange={(e) => setApiUrl(e.target.value)}
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* About Tab */}
              {activeTab === 'about' && (
                <div className="space-y-6">
                  <div className="border-b pb-3">
                    <h3 className="text-base font-bold text-slate-800 m-0">About Platform</h3>
                    <p className="text-xs text-slate-500 m-0">Hardware licensing details, versioning, and build profiles.</p>
                  </div>
                  
                  <div className="space-y-3 pt-4 text-xs font-medium text-slate-600 leading-relaxed">
                    <div>
                      <strong>Platform Name:</strong> InsightPilot Decision Intelligence
                    </div>
                    <div>
                      <strong>Software Version:</strong> 1.0.0 (Production Core release)
                    </div>
                    <div>
                      <strong>Engine Status:</strong> Deterministic Rule-Based Semantic Profiler Active
                    </div>
                    <div>
                      <strong>Built with:</strong> Python FastAPI, PostgreSQL SQLAlchemy, and React TypeScript with Vite.
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div className="text-[11px] text-slate-400 text-right font-semibold pt-6 border-t mt-6">
              InsightPilot Enterprise &bull; Version 1.0.0
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
