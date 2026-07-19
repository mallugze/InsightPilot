import { useEffect, useState } from 'react';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { apiFetch } from '../../../services/api';
import type { AnalysisResultResponse } from '../../../services/analysis';
import { Card } from '../../../components/ui/Card';
import { Button } from '../../../components/ui/Button';
import { Badge } from '../../../components/ui/Badge';
import { 
  FileText, 
  FileSpreadsheet, 
  Download, 
  Printer, 
  RefreshCw,
  AlertTriangle
} from 'lucide-react';

export default function ReportsPage() {
  const { uploadState } = useWorkspace();
  const [analysis, setAnalysis] = useState<AnalysisResultResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadReportData = async () => {
      if (!uploadState?.datasetId) {
        setLoading(false);
        return;
      }
      try {
        const data = await apiFetch<AnalysisResultResponse>(`/v1/analyze/${uploadState.datasetId}`);
        setAnalysis(data);
      } catch (err: any) {
        console.error("Failed to load analysis result for report:", err);
        setError("Please run the analysis pipeline first or select an active dataset.");
      } finally {
        setLoading(false);
      }
    };
    loadReportData();
  }, [uploadState?.datasetId]);

  const downloadJSON = () => {
    if (!analysis) return;
    const filename = `${analysis.semantic_profile?.suggested_workspace_name || 'insightpilot'}_report.json`;
    const blob = new Blob([JSON.stringify(analysis, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const triggerPrintReport = (reportType: 'summary' | 'profile' | 'analysis') => {
    if (!analysis) return;
    
    // Open a new popup print window
    const printWindow = window.open('', '_blank');
    if (!printWindow) {
      alert("Please allow popups to generate printable reports.");
      return;
    }

    const title = analysis.semantic_profile?.suggested_workspace_name || "InsightPilot Report";
    const domain = analysis.semantic_profile?.domain || "Standard";
    const subdomain = analysis.semantic_profile?.subdomain || "General";
    
    let contentHtml = '';
    
    if (reportType === 'summary') {
      contentHtml = `
        <div class="report-header">
          <h1>${title} - Executive Summary Report</h1>
          <p><strong>Domain:</strong> ${domain} &bull; <strong>Subdomain:</strong> ${subdomain}</p>
        </div>
        <div class="card">
          <h2>Executive Narrative Brief</h2>
          <p>${analysis.semantic_profile?.understanding_reasoning || 'No narrative brief found.'}</p>
        </div>
        <div class="card">
          <h2>Core Inferred KPIs</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>KPI Metric Name</th>
                <th>Aggregation Strategy</th>
                <th>Inferred target column</th>
                <th>KPI Reasoning</th>
              </tr>
            </thead>
            <tbody>
              ${(analysis.semantic_profile?.kpi_suggestions || []).map(k => `
                <tr>
                  <td><strong>${k.metric_name}</strong></td>
                  <td><code>${k.aggregation_strategy}</code></td>
                  <td><code>${k.target_column}</code></td>
                  <td>${k.reasoning}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
    } else if (reportType === 'profile') {
      contentHtml = `
        <div class="report-header">
          <h1>${title} - Dataset Profile Report</h1>
          <p><strong>Total samples:</strong> ${uploadState?.rowsCount || 'N/A'} &bull; <strong>Total Features:</strong> ${uploadState?.colsCount || 'N/A'}</p>
        </div>
        <div class="card">
          <h2>Column Feature Classifications</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>Column Name</th>
                <th>Semantic Type</th>
                <th>Native Type</th>
                <th>Confidence</th>
                <th>Possible Meaning</th>
              </tr>
            </thead>
            <tbody>
              ${(analysis.semantic_profile?.features || []).map(f => `
                <tr>
                  <td><code>${f.name}</code></td>
                  <td><span class="badge">${f.semantic_type}</span></td>
                  <td><code>${f.native_type}</code></td>
                  <td>${(f.confidence * 100).toFixed(0)}%</td>
                  <td><em>${f.possible_meaning}</em></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
    } else {
      contentHtml = `
        <div class="report-header">
          <h1>${title} - Predictive Modeling & ML Suitability Report</h1>
          <p><strong>Primary Target Inferred:</strong> <code>${analysis.semantic_profile?.relationships?.potential_targets?.[0] || 'None'}</code></p>
        </div>
        <div class="card">
          <h2>Machine Learning Readiness Evaluations</h2>
          <table class="data-table">
            <thead>
              <tr>
                <th>Task Type</th>
                <th>Viability Confidence</th>
                <th>Supporting Rationale</th>
              </tr>
            </thead>
            <tbody>
              ${Object.entries(analysis.semantic_profile?.ml_readiness || {}).map(([task, details]: any) => `
                <tr>
                  <td style="text-transform: capitalize;"><strong>${task}</strong></td>
                  <td><strong>${details.score}%</strong></td>
                  <td>${details.reasoning}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
        <div class="card">
          <h2>Recommended Modeling Algorithms</h2>
          <ul>
            ${(analysis.semantic_profile?.suggested_models || []).map(m => `
              <li>${m}</li>
            `).join('')}
          </ul>
        </div>
      `;
    }

    printWindow.document.write(`
      <html>
        <head>
          <title>${title} - Print Preview</title>
          <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #1e293b; padding: 40px; line-height: 1.6; }
            .report-header { border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 30px; }
            h1 { font-size: 24px; margin: 0; color: #0f172a; }
            h2 { font-size: 18px; color: #1e293b; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; margin-top: 0; }
            p { margin: 0 0 10px 0; }
            .card { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; margin-bottom: 24px; }
            .data-table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }
            .data-table th, .data-table td { padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: left; }
            .data-table th { background: #f8fafc; font-weight: bold; }
            code { font-family: monospace; background: #f1f5f9; padding: 2px 4px; border-radius: 4px; font-size: 12px; }
            .badge { background: #eff6ff; color: #1d4ed8; padding: 2px 6px; border-radius: 9999px; font-size: 11px; font-weight: bold; }
            @media print {
              body { padding: 0; }
              .card { border: none; padding: 0; margin-bottom: 30px; page-break-inside: avoid; }
            }
          </style>
        </head>
        <body>
          ${contentHtml}
          <script>
            window.onload = function() {
              window.print();
            }
          </script>
        </body>
      </html>
    `);
    printWindow.document.close();
  };

  if (!uploadState?.datasetId) {
    return (
      <main className="pt-12 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col justify-center items-center min-h-[50vh] gap-4 text-center">
        <AlertTriangle className="text-orange-500" size={40} />
        <h2 className="font-display text-xl font-bold text-slate-800">No Active Analysis Loaded</h2>
        <p className="font-sans text-sm text-slate-500 max-w-md">
          To generate executive reports, please select an active workspace dataset from the History page or upload a new file.
        </p>
      </main>
    );
  }

  if (loading) {
    return (
      <main className="pt-12 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col justify-center items-center min-h-[50vh] gap-4">
        <RefreshCw className="animate-spin text-secondary" size={32} />
        <p className="font-sans text-sm text-on-surface-variant font-medium">Preparing downloadable briefs...</p>
      </main>
    );
  }

  if (error || !analysis) {
    return (
      <main className="pt-12 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col justify-center items-center min-h-[50vh] gap-4 text-center">
        <AlertTriangle className="text-red-500" size={40} />
        <h2 className="font-display text-xl font-bold text-slate-800">Unable to Compile Reports</h2>
        <p className="font-sans text-sm text-slate-500 max-w-md">{error}</p>
      </main>
    );
  }

  const reportsList = [
    {
      id: 'summary',
      name: 'Executive Summary PDF',
      description: 'Contains overall business pulse ratings, core KPIs, and the analytical narrative brief.',
      action: () => triggerPrintReport('summary'),
      icon: <FileText className="text-red-600" size={24} />
    },
    {
      id: 'profile',
      name: 'Dataset Profile PDF',
      description: 'Contains full structural column metadata, semantic types, and missing data audits.',
      action: () => triggerPrintReport('profile'),
      icon: <FileSpreadsheet className="text-blue-600" size={24} />
    },
    {
      id: 'analysis',
      name: 'Machine Learning Readiness PDF',
      description: 'Contains explainable modeling feasibility scores and recommended prediction algorithms.',
      action: () => triggerPrintReport('analysis'),
      icon: <FileText className="text-purple-600" size={24} />
    }
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto pt-8 text-left px-margin-page pb-section-gap">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 m-0">Executive Reports Hub</h1>
        <p className="text-slate-500 mt-1">
          Compile summaries, classification grids, and model statistics for {analysis.semantic_profile?.suggested_workspace_name || 'your dataset'}.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {reportsList.map((rep) => (
          <Card key={rep.id} className="bg-white p-6 border rounded-xl flex flex-col justify-between min-h-[15rem] h-full shadow-sm hover:shadow-md transition-shadow">
            <div>
              <div className="flex items-center justify-between mb-4">
                <div className="p-2 bg-slate-50 rounded-lg">{rep.icon}</div>
                <Badge className="bg-slate-100 text-slate-700 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded">PDF Format</Badge>
              </div>
              <h3 className="text-base font-bold text-slate-800 m-0">{rep.name}</h3>
              <p className="text-xs text-slate-500 mt-2 leading-relaxed m-0 font-medium">{rep.description}</p>
            </div>
            <Button 
              onClick={rep.action}
              className="mt-4 bg-slate-50 hover:bg-slate-100 text-slate-700 font-bold border border-slate-200 py-2 rounded-lg flex items-center justify-center gap-2 cursor-pointer w-full text-xs"
            >
              <Printer size={14} />
              Print / Save PDF
            </Button>
          </Card>
        ))}
      </div>

      {/* Raw Exports Section */}
      <Card className="bg-white border rounded-xl p-6 shadow-sm text-left mt-8">
        <h3 className="text-lg font-bold text-slate-800 m-0 mb-2">Raw Data Exports</h3>
        <p className="text-xs text-slate-500 m-0 mb-6 font-medium">Export the raw analytical output variables or the complete raw CSV dataset.</p>
        <div className="flex flex-col sm:flex-row gap-4">
          <Button 
            onClick={downloadJSON}
            className="flex-1 bg-slate-900 hover:bg-slate-800 text-white font-semibold py-3 px-4 rounded-lg flex items-center justify-center gap-2 cursor-pointer text-sm"
          >
            <Download size={16} />
            Export Analysis JSON
          </Button>

          <a 
            href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/v1/datasets/${uploadState.datasetId}/download`}
            target="_blank"
            rel="noreferrer"
            className="flex-1 bg-primary text-on-primary hover:bg-inverse-surface font-semibold py-3 px-4 rounded-lg flex items-center justify-center gap-2 cursor-pointer text-sm text-center decoration-none"
          >
            <FileSpreadsheet size={16} />
            Export Raw Ingested CSV
          </a>
        </div>
      </Card>
    </div>
  );
}
