import { 
  Plus, 
  Search, 
  ChevronDown, 
  Heart, 
  BarChart2, 
  Database, 
  Table, 
  MoreVertical, 
  ChevronLeft, 
  ChevronRight, 
  Pin, 
  Clock, 
  FileText, 
  FileSpreadsheet, 
  Download 
} from 'lucide-react';
import { Card } from '../../../components/ui/Card';
import { Button } from '../../../components/ui/Button';
import { Badge } from '../../../components/ui/Badge';

export default function AnalysisHistoryPage() {
  const handleAction = (e: React.MouseEvent) => {
    e.preventDefault();
    alert('Action triggered');
  };

  return (
    <main className="pt-8 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col xl:flex-row gap-section-gap">
      {/* Left/Main Content */}
      <div className="flex-1 flex flex-col gap-stack-lg min-w-0">
        
        {/* Header Section */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div className="text-left">
            <h1 className="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface mb-2 m-0">
              Analysis History
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant m-0">
              Browse, revisit, and continue working with previous analyses.
            </p>
          </div>
          <Button 
            onClick={handleAction}
            className="hidden sm:flex bg-primary text-on-primary py-2 px-5 rounded-lg font-label-md text-label-md font-medium hover:bg-inverse-surface transition-colors shadow-sm items-center justify-center gap-2 whitespace-nowrap"
          >
            <Plus size={18} />
            New Analysis
          </Button>
        </div>

        {/* Controls Row */}
        <div className="flex flex-col md:flex-row gap-4 bg-surface-container-lowest p-4 rounded-xl border border-outline-variant shadow-sm text-left">
          {/* Search */}
          <div className="flex-1 relative min-w-[200px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant" size={20} />
            <input 
              className="w-full bg-surface-bright border border-outline-variant rounded-lg pl-10 pr-4 py-2 text-body-sm font-body-sm text-on-surface placeholder:text-on-surface-variant focus:outline-none focus:border-secondary focus:ring-2 focus:ring-secondary/20 transition-all" 
              placeholder="Search datasets, workspaces, or tags..." 
              type="text"
            />
          </div>

          {/* Filters */}
          <div className="flex flex-wrap items-center gap-3">
            <button className="flex items-center gap-2 px-3 py-2 border border-outline-variant rounded-lg text-body-sm font-label-md text-on-surface-variant hover:bg-surface-container-low transition-colors bg-surface-bright cursor-pointer font-medium">
              Dataset Type
              <ChevronDown size={16} />
            </button>
            <button className="flex items-center gap-2 px-3 py-2 border border-outline-variant rounded-lg text-body-sm font-label-md text-on-surface-variant hover:bg-surface-container-low transition-colors bg-surface-bright cursor-pointer font-medium">
              Date Range
              <ChevronDown size={16} />
            </button>
            <button className="flex items-center gap-2 px-3 py-2 border border-outline-variant rounded-lg text-body-sm font-label-md text-on-surface-variant hover:bg-surface-container-low transition-colors bg-surface-bright cursor-pointer font-medium">
              Status
              <ChevronDown size={16} />
            </button>
            <button className="flex items-center gap-2 px-3 py-2 border border-outline-variant rounded-full text-body-sm font-label-md text-on-surface-variant hover:bg-surface-container-low transition-colors bg-surface-bright cursor-pointer font-medium">
              <Heart size={18} />
              Favorites
            </button>
          </div>
        </div>

        {/* Analysis Table */}
        <Card className="bg-surface-container-lowest rounded-xl border border-outline-variant shadow-sm overflow-hidden flex-1 flex flex-col text-left">
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-outline-variant bg-surface-container-low/50">
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Dataset Name</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Upload Date</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Workspace</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Business Pulse</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">AI Confidence</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Insights</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap">Status</th>
                  <th className="px-6 py-4 font-label-caps text-label-caps text-on-surface-variant font-semibold whitespace-nowrap text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-outline-variant/50">
                {/* Row 1 */}
                <tr className="hover:bg-surface-container-low/30 transition-colors group cursor-pointer">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-[#F0F7FF] border border-[#3B82F6]/20 flex items-center justify-center text-[#3B82F6] shrink-0">
                        <BarChart2 size={18} />
                      </div>
                      <span className="font-label-md text-label-md text-on-surface group-hover:text-secondary transition-colors font-medium">Q3 Revenue Churn Model</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">Oct 24, 2023</td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">Finance Strategy</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-error"></div>
                      <span className="font-body-sm text-body-sm text-on-surface">Risk (42)</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface">94%</td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">12</td>
                  <td className="px-6 py-4">
                    <Badge className="inline-flex items-center px-2 py-1 rounded-full text-[11px] font-medium bg-surface-container-high text-on-surface-variant border border-outline-variant/50">
                      Completed
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-on-surface-variant hover:text-primary transition-colors p-1 rounded hover:bg-surface-container cursor-pointer">
                      <MoreVertical size={20} />
                    </button>
                  </td>
                </tr>

                {/* Row 2 */}
                <tr className="hover:bg-surface-container-low/30 transition-colors group cursor-pointer">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-[#F0F7FF] border border-[#3B82F6]/20 flex items-center justify-center text-[#3B82F6] shrink-0">
                        <Database size={18} />
                      </div>
                      <span className="font-label-md text-label-md text-on-surface group-hover:text-secondary transition-colors font-medium">Customer Sentiment Q3</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">Oct 22, 2023</td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">Marketing</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-[#10B981]"></div>
                      <span className="font-body-sm text-body-sm text-on-surface">Growth (88)</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface">89%</td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">8</td>
                  <td className="px-6 py-4">
                    <Badge className="inline-flex items-center px-2 py-1 rounded-full text-[11px] font-medium bg-surface-container-high text-on-surface-variant border border-outline-variant/50">
                      Completed
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-on-surface-variant hover:text-primary transition-colors p-1 rounded hover:bg-surface-container cursor-pointer">
                      <MoreVertical size={20} />
                    </button>
                  </td>
                </tr>

                {/* Row 3 */}
                <tr className="hover:bg-surface-container-low/30 transition-colors group cursor-pointer">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-surface-container border border-outline-variant/50 flex items-center justify-center text-on-surface-variant shrink-0">
                        <Database size={18} />
                      </div>
                      <span className="font-label-md text-label-md text-on-surface group-hover:text-secondary transition-colors font-medium">Supply Chain Latency - APAC</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">Oct 20, 2023</td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">Operations</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-[#F59E0B]"></div>
                      <span className="font-body-sm text-body-sm text-on-surface">Caution (65)</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant/50">--</td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant/50">--</td>
                  <td className="px-6 py-4">
                    <Badge className="inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-[11px] font-medium bg-secondary/10 text-secondary border border-secondary/20">
                      <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
                      Processing
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-on-surface-variant hover:text-primary transition-colors p-1 rounded hover:bg-surface-container cursor-pointer">
                      <MoreVertical size={20} />
                    </button>
                  </td>
                </tr>

                {/* Row 4 */}
                <tr className="hover:bg-surface-container-low/30 transition-colors group cursor-pointer opacity-75">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-surface-container border border-outline-variant/50 flex items-center justify-center text-on-surface-variant shrink-0">
                        <Table size={18} />
                      </div>
                      <span className="font-label-md text-label-md text-on-surface group-hover:text-secondary transition-colors font-medium">Legacy CRM Export 2022</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">Oct 18, 2023</td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant">Archive</td>
                  <td className="px-6 py-4">
                    <span className="font-body-sm text-body-sm text-on-surface-variant">N/A</span>
                  </td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant/50">--</td>
                  <td className="px-6 py-4 font-body-sm text-body-sm text-on-surface-variant/50">--</td>
                  <td className="px-6 py-4">
                    <Badge className="inline-flex items-center px-2 py-1 rounded-full text-[11px] font-medium bg-error/10 text-error border border-error/20">
                      Failed
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-on-surface-variant hover:text-primary transition-colors p-1 rounded hover:bg-surface-container cursor-pointer">
                      <MoreVertical size={20} />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between px-6 py-4 border-t border-outline-variant/50 bg-surface-bright">
            <span className="font-body-sm text-body-sm text-on-surface-variant font-medium">Showing 1 to 4 of 24 entries</span>
            <div className="flex items-center gap-2">
              <button className="p-1 rounded border border-outline-variant text-on-surface-variant disabled:opacity-50 cursor-not-allowed" disabled>
                <ChevronLeft size={18} />
              </button>
              <button className="p-1 rounded border border-outline-variant text-on-surface-variant hover:bg-surface-container-low transition-colors cursor-pointer">
                <ChevronRight size={18} />
              </button>
            </div>
          </div>
        </Card>
      </div>

      {/* Right Sidebar (Recent Activity) */}
      <aside className="w-full xl:w-[320px] flex flex-col gap-stack-lg shrink-0 text-left">
        {/* Pinned Analyses */}
        <Card className="bg-surface-container-lowest rounded-xl border border-outline-variant p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Pin className="text-secondary" size={20} />
            <h3 className="font-label-md text-label-md font-semibold text-on-surface uppercase tracking-wide m-0">Pinned Analyses</h3>
          </div>
          <ul className="space-y-3 p-0 m-0 list-none">
            <li>
              <a className="flex flex-col gap-1 p-3 rounded-lg border border-outline-variant/50 hover:border-secondary/50 hover:bg-[#F0F7FF] transition-all group" href="#">
                <span className="font-label-md text-label-md text-on-surface group-hover:text-secondary font-medium">Global Sales Forecast FY24</span>
                <span className="font-body-sm text-body-sm text-on-surface-variant text-[12px]">Last updated 2 days ago</span>
              </a>
            </li>
            <li>
              <a className="flex flex-col gap-1 p-3 rounded-lg border border-outline-variant/50 hover:border-secondary/50 hover:bg-[#F0F7FF] transition-all group" href="#">
                <span className="font-label-md text-label-md text-on-surface group-hover:text-secondary font-medium">Competitor Pricing Matrix</span>
                <span className="font-body-sm text-body-sm text-on-surface-variant text-[12px]">Last updated 1 week ago</span>
              </a>
            </li>
          </ul>
        </Card>

        {/* Recently Opened */}
        <Card className="bg-surface-container-lowest rounded-xl border border-outline-variant p-6 shadow-sm">
          <h3 className="font-label-caps text-label-caps text-on-surface-variant font-medium mb-4 m-0 uppercase tracking-wider">Recently Opened</h3>
          <ul className="space-y-4 p-0 m-0 list-none">
            <li className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center shrink-0 mt-0.5">
                <Clock className="text-on-surface-variant" size={16} />
              </div>
              <div>
                <a className="font-label-md text-label-md text-on-surface hover:text-secondary transition-colors block mb-0.5 font-medium" href="#">Q3 Revenue Churn Model</a>
                <p className="font-body-sm text-body-sm text-on-surface-variant text-[12px] m-0">Opened 2 hours ago by You</p>
              </div>
            </li>
            <li className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center shrink-0 mt-0.5">
                <Clock className="text-on-surface-variant" size={16} />
              </div>
              <div>
                <a className="font-label-md text-label-md text-on-surface hover:text-secondary transition-colors block mb-0.5 font-medium" href="#">Customer Sentiment Q3</a>
                <p className="font-body-sm text-body-sm text-on-surface-variant text-[12px] m-0">Opened yesterday by David C.</p>
              </div>
            </li>
          </ul>
        </Card>

        {/* Recent Exports */}
        <Card className="bg-surface-container-lowest rounded-xl border border-outline-variant p-6 shadow-sm">
          <h3 className="font-label-caps text-label-caps text-on-surface-variant font-medium mb-4 m-0 uppercase tracking-wider">Recent Exports</h3>
          <ul className="space-y-3 p-0 m-0 list-none">
            <li className="flex items-center justify-between p-2 hover:bg-surface-container-low rounded-lg transition-colors group">
              <div className="flex items-center gap-3">
                <FileText className="text-[#E11D48] shrink-0" size={20} />
                <span className="font-body-sm text-body-sm text-on-surface font-medium">Executive Summary</span>
              </div>
              <button className="opacity-0 group-hover:opacity-100 transition-opacity text-on-surface-variant hover:text-primary cursor-pointer">
                <Download size={18} />
              </button>
            </li>
            <li className="flex items-center justify-between p-2 hover:bg-surface-container-low rounded-lg transition-colors group">
              <div className="flex items-center gap-3">
                <FileSpreadsheet className="text-[#16A34A] shrink-0" size={20} />
                <span className="font-body-sm text-body-sm text-on-surface font-medium">Raw Dataset_v2</span>
              </div>
              <button className="opacity-0 group-hover:opacity-100 transition-opacity text-on-surface-variant hover:text-primary cursor-pointer">
                <Download size={18} />
              </button>
            </li>
          </ul>
        </Card>
      </aside>
    </main>
  );
}
