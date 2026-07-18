import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Plus, 
  Search, 
  Pin, 
  RefreshCw
} from 'lucide-react';
import { Card } from '../../../components/ui/Card';
import { Button } from '../../../components/ui/Button';
import { Badge } from '../../../components/ui/Badge';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { apiFetch } from '../../../services/api';

export default function AnalysisHistoryPage() {
  const [historyItems, setHistoryItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  
  const { startUpload, completeAnalysis, confirmWorkspace, resetOnboardingKeepProfile } = useWorkspace();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await apiFetch<any[]>('/v1/analyze/history');
        setHistoryItems(data);
      } catch (err: any) {
        console.error("Failed to load analysis history:", err);
        console.warn("Failed to load history list.");
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const handleReopen = (item: any) => {
    // 1. Stage upload context
    startUpload({
      fileName: item.dataset_name,
      fileSize: "N/A",
      datasetId: String(item.dataset_id),
      datasetType: item.domain,
      rowsCount: item.rows,
      colsCount: item.columns,
    });
    
    // 2. Complete onboarding analysis configurations
    completeAnalysis(
      item.domain,
      item.rows,
      item.columns,
      item.business_pulse || 95,
      `Reopened existing database analysis for dataset '${item.dataset_name}'.`,
      item.workspace_name,
      String(item.dataset_id),
      item.dataset_name
    );
    
    // 3. Confirm active workspace
    confirmWorkspace(item.workspace_name);
    
    // 4. Redirect to dashboard view
    navigate('/dashboard');
  };

  const getDomainIcon = (domain: string) => {
    const domLower = (domain || '').toLowerCase();
    if (domLower.includes('scientific') || domLower.includes('biology')) return '🌸';
    if (domLower.includes('machine learning') || domLower.includes('classification')) return '🤖';
    if (domLower.includes('sales') || domLower.includes('business')) return '📈';
    if (domLower.includes('healthcare') || domLower.includes('clinical')) return '🏥';
    if (domLower.includes('real estate') || domLower.includes('valuation')) return '🏠';
    if (domLower.includes('iot') || domLower.includes('telemetry')) return '🌦';
    if (domLower.includes('finance')) return '💼';
    if (domLower.includes('hr') || domLower.includes('human')) return '👥';
    return '📊';
  };

  const filteredItems = historyItems.filter(item => {
    const query = searchQuery.toLowerCase();
    return (
      item.dataset_name.toLowerCase().includes(query) ||
      item.workspace_name.toLowerCase().includes(query) ||
      item.domain.toLowerCase().includes(query)
    );
  });

  const pinnedItems = historyItems.filter(item => (item.business_pulse || 0) >= 80).slice(0, 3);
  const recentItems = historyItems.slice(0, 3);

  if (loading) {
    return (
      <main className="pt-12 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col justify-center items-center min-h-[60vh] gap-4">
        <RefreshCw className="animate-spin text-secondary" size={32} style={{ animationDuration: '2s' }} />
        <p className="font-sans text-sm text-on-surface-variant font-medium">Retrieving active profiles from PostgreSQL...</p>
      </main>
    );
  }

  return (
    <main className="pt-8 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col xl:flex-row gap-section-gap">
      {/* Left/Main Content */}
      <div className="flex-1 flex flex-col gap-stack-lg min-w-0">
        
        {/* Header Section */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div className="text-left">
            <h1 className="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface mb-2 m-0 font-bold">
              Analysis History
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant m-0">
              Browse, revisit, and continue working with database records.
            </p>
          </div>
          <Button 
            onClick={() => {
              resetOnboardingKeepProfile();
              navigate('/upload');
            }}
            className="flex bg-primary text-on-primary py-2.5 px-5 rounded-lg font-label-md text-label-md font-medium hover:bg-inverse-surface transition-colors shadow-sm items-center justify-center gap-2 whitespace-nowrap cursor-pointer"
          >
            <Plus size={18} />
            New Ingestion
          </Button>
        </div>

        {/* Controls Row */}
        <div className="flex flex-col md:flex-row gap-4 bg-surface-container-lowest p-4 rounded-xl border border-outline-variant shadow-sm text-left">
          {/* Search */}
          <div className="flex-1 relative min-w-[200px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant" size={20} />
            <input 
              className="w-full bg-surface-bright border border-outline-variant rounded-lg pl-10 pr-4 py-2 text-body-sm font-body-sm text-on-surface placeholder:text-on-surface-variant focus:outline-none focus:border-secondary focus:ring-2 focus:ring-secondary/20 transition-all" 
              placeholder="Search datasets, workspaces, or domains..." 
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        {/* Table Card */}
        <Card className="bg-surface-container-lowest rounded-xl border border-outline-variant shadow-sm overflow-hidden flex-1 flex flex-col text-left">
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-outline-variant bg-surface-container-low/50">
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Dataset Name</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Upload Date</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Workspace</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Domain</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Samples</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Pulse</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Match</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant/50">
                {filteredItems.length > 0 ? (
                  filteredItems.map((item) => (
                    <tr 
                      key={item.dataset_id} 
                      onClick={() => handleReopen(item)}
                      className="hover:bg-slate-50/50 transition-colors group cursor-pointer"
                    >
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-center text-lg shrink-0">
                            {getDomainIcon(item.domain)}
                          </div>
                          <span className="font-label-md text-label-md text-on-surface group-hover:text-secondary transition-colors font-semibold">
                            {item.dataset_name}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">
                        {item.upload_date ? new Date(item.upload_date).toLocaleDateString(undefined, {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric'
                        }) : 'N/A'}
                      </td>
                      <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant font-medium">
                        {item.workspace_name}
                      </td>
                      <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">
                        <Badge className="bg-secondary/5 text-secondary border border-secondary/15 px-2 py-0.5 rounded text-[11px] font-semibold">
                          {item.domain}
                        </Badge>
                      </td>
                      <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant font-bold">
                        {item.rows.toLocaleString()} x {item.columns}
                      </td>
                      <td className="px-6 py-4">
                        {item.business_pulse !== null ? (
                          <div className="flex items-center gap-2">
                            <div className={`w-2 h-2 rounded-full ${
                              item.business_pulse >= 80 ? 'bg-emerald-500' :
                              item.business_pulse >= 50 ? 'bg-amber-500' : 'bg-red-500'
                            }`}></div>
                            <span className="font-body-sm text-body-sm text-on-surface font-semibold">
                              {item.business_pulse}/100
                            </span>
                          </div>
                        ) : (
                          <span className="text-slate-400 italic">Unprocessed</span>
                        )}
                      </td>
                      <td className="px-6 py-4 font-body-sm text-body-sm text-slate-800 font-bold">
                        {(item.overall_confidence * 100).toFixed(0)}%
                      </td>
                      <td className="px-6 py-4">
                        <Badge className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                          item.status === 'READY' ? 'bg-emerald-50 text-emerald-700 border border-emerald-100' :
                          item.status === 'FAILED' ? 'bg-red-50 text-red-700 border border-red-100' :
                          'bg-amber-50 text-amber-700 border border-amber-100 animate-pulse'
                        }`}>
                          {item.status}
                        </Badge>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={8} className="px-6 py-12 text-center text-slate-400 italic">
                      No analysis histories found. Ingest your first dataset!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      {/* Right Sidebar (Recent Activity) */}
      <aside className="w-full xl:w-[320px] flex flex-col gap-stack-lg shrink-0 text-left">
        {/* Pinned Analyses */}
        <Card className="bg-surface-container-lowest rounded-xl border border-outline-variant p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Pin className="text-secondary" size={20} />
            <h3 className="font-label-md text-label-md font-semibold text-on-surface uppercase tracking-wide m-0">Top Active Analyses</h3>
          </div>
          {pinnedItems.length > 0 ? (
            <ul className="space-y-3 p-0 m-0 list-none">
              {pinnedItems.map((item) => (
                <li key={item.dataset_id}>
                  <div 
                    onClick={() => handleReopen(item)}
                    className="flex flex-col gap-1 p-3 rounded-lg border border-outline-variant/50 hover:border-secondary/50 hover:bg-[#F0F7FF] transition-all group cursor-pointer"
                  >
                    <span className="font-label-md text-label-md text-on-surface group-hover:text-secondary font-bold flex items-center gap-1.5">
                      <span>{getDomainIcon(item.domain)}</span>
                      <span className="truncate">{item.dataset_name}</span>
                    </span>
                    <span className="font-body-sm text-body-sm text-on-surface-variant text-[11px] font-semibold">
                      Pulse: {item.business_pulse}/100 • {item.domain}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-slate-400 italic m-0">No top analysis records available.</p>
          )}
        </Card>

        {/* Recently Opened */}
        <Card className="bg-surface-container-lowest rounded-xl border border-outline-variant p-6 shadow-sm">
          <h3 className="font-label-caps text-label-caps text-on-surface-variant font-medium mb-4 m-0 uppercase tracking-wider">Recently Uploaded</h3>
          {recentItems.length > 0 ? (
            <ul className="space-y-4 p-0 m-0 list-none">
              {recentItems.map((item) => (
                <li 
                  key={item.dataset_id} 
                  onClick={() => handleReopen(item)}
                  className="flex items-start gap-3 cursor-pointer group"
                >
                  <div className="w-8 h-8 rounded-full bg-slate-50 border flex items-center justify-center shrink-0 text-sm">
                    {getDomainIcon(item.domain)}
                  </div>
                  <div>
                    <span className="font-label-md text-label-md text-on-surface group-hover:text-secondary transition-colors block mb-0.5 font-bold truncate max-w-[180px]">
                      {item.dataset_name}
                    </span>
                    <p className="font-body-sm text-body-sm text-on-surface-variant text-[11px] m-0 font-medium">
                      {item.rows.toLocaleString()} rows • {item.domain}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-slate-400 italic m-0">No recent datasets listed.</p>
          )}
        </Card>
      </aside>
    </main>
  );
}
