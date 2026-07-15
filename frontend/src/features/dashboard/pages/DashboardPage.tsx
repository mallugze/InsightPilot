import { useEffect, useState } from 'react';
import { 
  Activity, 
  Sparkles, 
  AlertTriangle, 
  Award, 
  TrendingDown, 
  Lightbulb, 
  MoreVertical, 
  Brain, 
  Check, 
  RefreshCw,
  Info
} from 'lucide-react';
import { Card } from '../../../components/ui/Card';
import { Button } from '../../../components/ui/Button';
import { Badge } from '../../../components/ui/Badge';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { getAnalysisResult, runDatasetAnalysis } from '../../../services/analysis';
import type { AnalysisResultResponse } from '../../../services/analysis';

export default function DashboardPage() {
  const { uploadState } = useWorkspace();
  const [analysis, setAnalysis] = useState<AnalysisResultResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reanalyzing, setReanalyzing] = useState(false);

  const fetchAnalysis = async (forceTrigger = false) => {
    if (!uploadState?.datasetId) {
      setError("No active dataset uploaded. Please return to landing flow to ingest a CSV/Excel file.");
      setLoading(false);
      return;
    }
    
    try {
      if (forceTrigger) {
        setReanalyzing(true);
      }
      const datasetIdNum = parseInt(uploadState.datasetId, 10);
      
      let data: AnalysisResultResponse;
      if (forceTrigger) {
        data = await runDatasetAnalysis(datasetIdNum);
      } else {
        try {
          data = await getAnalysisResult(datasetIdNum);
        } catch {
          // If not cached yet, trigger POST
          data = await runDatasetAnalysis(datasetIdNum);
        }
      }
      
      setAnalysis(data);
      setError(null);
    } catch (err: any) {
      console.error("Failed to load dashboard metrics:", err);
      setError(err.message || "Failed to load active analysis profile from backend.");
    } finally {
      setLoading(false);
      setReanalyzing(false);
    }
  };

  useEffect(() => {
    fetchAnalysis();
  }, [uploadState?.datasetId]);

  if (loading) {
    return (
      <main className="pt-12 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col justify-center items-center min-h-[60vh] gap-4">
        <RefreshCw className="animate-spin text-secondary" size={32} />
        <p className="font-sans text-sm text-on-surface-variant font-medium">Assembling dashboard from database profiles...</p>
      </main>
    );
  }

  if (error || !analysis) {
    return (
      <main className="pt-12 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col justify-center items-center min-h-[60vh] gap-4 text-center">
        <AlertTriangle className="text-orange-500" size={40} />
        <h2 className="font-display text-2xl font-bold text-primary">Unable to load analytics</h2>
        <p className="font-sans text-sm text-on-surface-variant max-w-md">{error || "Verify backend service runs and dataset is loaded."}</p>
        <Button onClick={() => fetchAnalysis(true)} className="bg-primary text-white font-semibold px-4 py-2 rounded-lg mt-2">
          Retry Analysis Pipeline
        </Button>
      </main>
    );
  }

  // Helper variables for rendering
  const pulse = analysis.business_pulse;
  const healthLabel = analysis.health_label;
  const breakdown = analysis.pulse_breakdown || { data_quality: 100, completeness: 100, consistency: 100, business_performance: 100 };
  const kpis = analysis.kpis || {};
  const hero = analysis.hero || { hero_name: 'N/A', hero_value: 0, zero_name: 'N/A', zero_value: 0, reason: 'N/A' };
  const trends = analysis.trends || { has_trends: false, chart_data: [] };
  const anomalies = analysis.anomalies || { anomalies_count: 0, anomalies: [] };
  const correlations = analysis.correlations || { correlations: [] };
  const recommendations = analysis.recommendations || [];
  const insights = analysis.insights || [];

  // Determine pulse bullet color
  const pulseColor = pulse >= 90 ? 'bg-emerald-500' :
                     pulse >= 75 ? 'bg-teal-500' :
                     pulse >= 50 ? 'bg-amber-500' :
                     pulse >= 30 ? 'bg-orange-500' : 'bg-red-500';

  const pulseTextClass = pulse >= 75 ? 'text-emerald-700' :
                         pulse >= 50 ? 'text-amber-700' : 'text-red-700';

  return (
    <main className="pt-8 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col gap-section-gap antialiased text-left">
      {/* Top Section: Pulse & Hero Brief */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
        {/* Business Pulse Scorecard (Col 1-3) */}
        <Card className="lg:col-span-3 bg-surface rounded-lg card-border p-gutter flex flex-col justify-between hover:shadow-[0_4px_6px_-1px_rgb(0,0,0,0.05)] transition-shadow text-left">
          <div>
            <div className="flex justify-between items-start mb-stack-sm">
              <h3 className="font-label-caps text-label-caps text-on-surface-variant m-0">Business Pulse</h3>
              <Activity className="text-secondary animate-pulse" size={20} />
            </div>
            <div className="flex items-baseline gap-2 mb-unit">
              <span className="font-display-lg text-display-lg text-on-surface font-extrabold">{pulse}</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant">/100</span>
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-2.5 h-2.5 rounded-full ${pulseColor}`}></div>
              <span className={`font-label-md text-label-md font-bold ${pulseTextClass}`}>{healthLabel}</span>
            </div>
          </div>
          <div className="mt-stack-md pt-stack-md border-t border-outline-variant/30 space-y-2.5">
            <div className="flex justify-between text-sm">
              <span className="font-body-sm text-body-sm text-on-surface-variant">Data Quality</span>
              <span className="font-label-md text-label-md text-on-surface font-semibold">{breakdown.data_quality}%</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="font-body-sm text-body-sm text-on-surface-variant">Completeness</span>
              <span className="font-label-md text-label-md text-on-surface font-semibold">{breakdown.completeness}%</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="font-body-sm text-body-sm text-on-surface-variant">Consistency</span>
              <span className="font-label-md text-label-md text-on-surface font-semibold">{breakdown.consistency}%</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="font-body-sm text-body-sm text-on-surface-variant">Performance</span>
              <span className="font-label-md text-label-md text-on-surface font-semibold">{breakdown.business_performance}%</span>
            </div>
          </div>
        </Card>

        {/* Today's Brief (Executive Summary from Insights) (Col 4-12) */}
        <div className="lg:col-span-9 bg-[#F0F7FF] rounded-lg card-border ai-accent-border p-[32px] hover:shadow-[0_4px_6px_-1px_rgb(0,0,0,0.05)] transition-shadow text-left flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-stack-md">
              <Sparkles className="text-secondary" size={20} />
              <h2 className="font-headline-md text-headline-md text-on-surface m-0 font-bold">Executive Insights Brief</h2>
              <Badge className="ml-auto font-label-caps text-label-caps bg-secondary/10 text-secondary px-3 py-1 rounded-full border border-secondary/15 font-semibold">
                Deterministic Profile
              </Badge>
            </div>
            <div className="prose prose-sm max-w-none text-on-surface font-body-lg text-body-lg leading-relaxed space-y-3 pr-2">
              {insights.length > 0 ? (
                insights.map((insight, idx) => (
                  <p key={idx} className="m-0 font-medium text-slate-800">
                    • {insight}
                  </p>
                ))
              ) : (
                <p>No deterministic insights found. Dataset columns lack semantic parameters.</p>
              )}
            </div>
          </div>
          <div className="mt-stack-lg flex gap-stack-md">
            <Button 
              onClick={() => fetchAnalysis(true)}
              disabled={reanalyzing}
              className="bg-primary text-on-primary font-label-md text-label-md px-4 py-2 rounded-lg flex items-center gap-2 font-semibold hover:bg-slate-800 transition-colors"
            >
              <RefreshCw size={16} className={reanalyzing ? "animate-spin" : ""} />
              {reanalyzing ? "Re-calculating..." : "Recalculate Metrics"}
            </Button>
          </div>
        </div>
      </section>

      {/* SECTION 1: Business Signals (Dynamic KPIs) */}
      <section className="space-y-4">
        <h3 className="font-headline-md text-headline-md text-on-surface m-0 font-bold">Key Performance Indicators</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-stack-md">
          {Object.entries(kpis).map(([key, value]) => {
            const displayKey = key.replace(/_/g, ' ').toUpperCase();
            
            // Render nice formats
            let displayVal = "";
            if (typeof value === "number") {
              if (key.includes("revenue") || key.includes("profit") || key.includes("salary") || key.includes("income") || key.includes("expense") || key.includes("value") || key.includes("sum")) {
                displayVal = `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
              } else if (key.includes("margin") || key.includes("rate") || key.includes("percent")) {
                displayVal = `${value}%`;
              } else {
                displayVal = value.toLocaleString();
              }
            } else {
              displayVal = String(value);
            }
            
            return (
              <Card key={key} className="bg-surface rounded-lg card-border p-stack-md flex flex-col justify-between text-left h-28 hover:shadow-sm transition-shadow">
                <span className="font-label-caps text-label-caps text-on-surface-variant font-bold block truncate">{displayKey}</span>
                <div className="flex items-baseline mt-auto">
                  <span className="font-headline-md text-headline-md text-on-surface font-extrabold truncate">{displayVal}</span>
                </div>
              </Card>
            );
          })}
        </div>
      </section>

      {/* Dataset Intelligence Panel */}
      <section className="space-y-4">
        <Card className="bg-white rounded-lg card-border p-gutter flex flex-col gap-4 text-left border border-slate-200 shadow-sm">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3 justify-between">
            <div className="flex items-center gap-2">
              <Brain className="text-secondary" size={24} />
              <div>
                <h3 className="font-display text-lg font-bold text-slate-800 m-0">Dataset Intelligence Panel</h3>
                <p className="font-sans text-xs text-slate-500 m-0">Hierarchical semantic profiles, column meanings, and machine learning readiness details.</p>
              </div>
            </div>
            {analysis.semantic_profile && (
              <Badge className="bg-emerald-50 text-emerald-700 border border-emerald-100 font-semibold px-2.5 py-1 rounded text-xs">
                Inferred: {analysis.semantic_profile.domain} Domain ({analysis.semantic_profile.subdomain})
              </Badge>
            )}
          </div>
          
          {analysis.semantic_profile ? (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
              {/* Classification Description */}
              <div className="lg:col-span-8 space-y-5">
                <div className="bg-primary/5 rounded-lg p-4 border border-primary/10">
                  <h4 className="font-display text-sm font-semibold text-primary mb-1.5 flex items-center gap-1.5">
                    <Sparkles size={16} /> Analytical Reasoning Summary
                  </h4>
                  <p className="font-sans text-sm text-slate-700 leading-relaxed m-0 font-medium">
                    {analysis.semantic_profile.understanding_reasoning}
                  </p>
                </div>
                
                {/* Features List */}
                <div>
                  <h4 className="font-display text-sm font-semibold text-slate-800 mb-2">Column Feature Classifications</h4>
                  <div className="overflow-x-auto">
                    <table className="min-w-full text-xs divide-y divide-slate-100">
                      <thead>
                        <tr className="text-slate-500 font-bold text-[11px] uppercase tracking-wider bg-slate-50/50">
                          <th className="py-2.5 px-3 text-left">Column</th>
                          <th className="py-2.5 px-3 text-left">Semantic Type</th>
                          <th className="py-2.5 px-3 text-left">Native Type</th>
                          <th className="py-2.5 px-3 text-left">Confidence</th>
                          <th className="py-2.5 px-3 text-left">Possible Meaning</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100 text-slate-700 bg-white">
                        {analysis.semantic_profile.features.map((f, i) => (
                          <tr key={i} className="hover:bg-slate-50/30 transition-colors">
                            <td className="py-2.5 px-3 font-mono text-secondary font-bold text-xs">{f.name}</td>
                            <td className="py-2.5 px-3">
                              <Badge className="bg-secondary/10 text-secondary text-[10px] px-2.5 py-0.5 rounded font-bold border border-secondary/15">
                                {f.semantic_type}
                              </Badge>
                            </td>
                            <td className="py-2.5 px-3 text-slate-500 font-mono text-xs">{f.native_type}</td>
                            <td className="py-2.5 px-3 font-bold text-emerald-600">{(f.confidence * 100).toFixed(0)}%</td>
                            <td className="py-2.5 px-3 text-slate-500 italic">{f.possible_meaning}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              {/* Hierarchical metadata & ML Readiness Info (Col 4) */}
              <div className="lg:col-span-4 space-y-4">
                <div className="bg-slate-50/50 rounded-lg p-4 border border-slate-100 space-y-3">
                  <h4 className="font-display text-sm font-semibold text-slate-800 border-b border-slate-200/60 pb-1.5 m-0">
                    Semantic Hierarchy
                  </h4>
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">Top-Level Domain:</span>
                      <span className="font-bold text-secondary text-right">{analysis.semantic_profile.domain}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">Subdomain:</span>
                      <span className="font-semibold text-slate-800 text-right">{analysis.semantic_profile.subdomain}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">Confidence Rating:</span>
                      <span className="font-bold text-emerald-600">{(analysis.semantic_profile.domain_confidence * 100).toFixed(0)}%</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">Row Entity Item:</span>
                      <span className="font-mono bg-slate-200/50 px-2 py-0.5 rounded text-slate-700 font-bold">{analysis.semantic_profile.entity}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-slate-50/50 rounded-lg p-4 border border-slate-100 space-y-3">
                  <h4 className="font-display text-sm font-semibold text-slate-800 border-b border-slate-200/60 pb-1.5 m-0">
                    Machine Learning Readiness
                  </h4>
                  <div className="space-y-3">
                    {Object.entries(analysis.semantic_profile.ml_readiness).map(([task, details]: any) => (
                      <div key={task} className="text-xs space-y-1 bg-white p-2.5 rounded-lg border border-slate-200/60 shadow-[0_1px_2px_0_rgba(0,0,0,0.02)]">
                        <div className="flex justify-between items-center">
                          <span className="font-bold text-slate-700 capitalize">{task}</span>
                          <span className={`font-bold px-2 py-0.5 rounded text-[10px] uppercase border ${
                            details.score >= 70 ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
                            details.score >= 40 ? 'bg-amber-50 text-amber-700 border-amber-100' :
                            'bg-red-50 text-red-700 border-red-100'
                          }`}>
                            {details.score}%
                          </span>
                        </div>
                        <p className="text-[10px] text-slate-500 leading-tight m-0 font-medium pt-1">
                          {details.reasoning}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-sm text-slate-500 italic m-0">No semantic metadata profiles exist in the active report.</p>
          )}
        </Card>
      </section>

      {/* SECTION 2: Hero & Zero */}
      {hero.metric_name !== "None" && (
        <section className="space-y-4">
          <h3 className="font-headline-md text-headline-md text-on-surface m-0 font-bold">Performance Bounds</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
            {/* Hero Card */}
            <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col text-left hover:shadow-sm transition-all border-l-4 border-l-emerald-500">
              <div className="flex items-center gap-2 mb-stack-md">
                <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-700 shrink-0">
                  <Award size={16} />
                </div>
                <h3 className="font-headline-md text-headline-md text-on-surface m-0 font-bold">
                  Top Category: {hero.hero_name}
                </h3>
              </div>
              <p className="font-body-md text-body-md text-on-surface-variant mb-stack-md leading-relaxed">
                {hero.reason}
              </p>
              <div className="mt-auto bg-surface-container-low p-stack-md rounded-lg border border-outline-variant/30 flex items-start gap-stack-sm">
                <Lightbulb size={16} className="text-secondary mt-0.5" />
                <div>
                  <span className="font-label-md text-label-md text-on-surface block mb-1 font-bold">Performance Value</span>
                  <span className="font-body-sm text-body-sm text-on-surface-variant block font-medium">
                    Total {hero.metric_name}: ${hero.hero_value?.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                  </span>
                </div>
              </div>
            </Card>

            {/* Zero Card */}
            <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col text-left hover:shadow-sm transition-all border-l-4 border-l-orange-500">
              <div className="flex items-center gap-2 mb-stack-md">
                <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center text-orange-700 shrink-0">
                  <TrendingDown size={16} />
                </div>
                <h3 className="font-headline-md text-headline-md text-on-surface m-0 font-bold">
                  Underperforming Category: {hero.zero_name}
                </h3>
              </div>
              <p className="font-body-md text-body-md text-on-surface-variant mb-stack-md leading-relaxed">
                Aggregating the {hero.group_by_column} group identifies '{hero.zero_name}' as the lowest performance segment, requiring operational attention.
              </p>
              <div className="mt-auto bg-surface-container-low p-stack-md rounded-lg border border-outline-variant/30 flex items-start gap-stack-sm">
                <Lightbulb size={16} className="text-secondary mt-0.5" />
                <div>
                  <span className="font-label-md text-label-md text-on-surface block mb-1 font-bold">Performance Value</span>
                  <span className="font-body-sm text-body-sm text-on-surface-variant block font-medium">
                    Total {hero.metric_name}: ${hero.zero_value?.toLocaleString(undefined, { minimumFractionDigits: 2 })}
                  </span>
                </div>
              </div>
            </Card>
          </div>
        </section>
      )}

      {/* SECTION 3: Smart Charts & Outliers */}
      <section className="space-y-4">
        <h3 className="font-headline-md text-headline-md text-on-surface m-0 font-bold">Supporting Analytics</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
          {/* Timeline Trend Line Chart */}
          <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col h-80 text-left hover:shadow-sm transition-shadow">
            <div className="flex justify-between items-center mb-stack-md">
              <div>
                <h4 className="font-label-md text-label-md text-on-surface m-0 font-bold">
                  {trends.has_trends ? `${trends.metric_name} Trend (${trends.period.toUpperCase()})` : "Timeline Trend"}
                </h4>
                {trends.has_trends && (
                  <span className="text-xs text-on-surface-variant">
                    Direction: <strong className="text-secondary">{trends.trend_direction}</strong> | Growth: <strong className="text-emerald-600">+{trends.growth_percent}%</strong>
                  </span>
                )}
              </div>
              <MoreVertical className="text-on-surface-variant" size={16} />
            </div>
            
            {trends.has_trends && trends.chart_data.length > 1 ? (
              <div className="flex-1 relative flex flex-col justify-between pt-2">
                {/* SVG Line & Area Graphic */}
                <div className="flex-1 relative">
                  <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 50">
                    <defs>
                      <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#2170e4" stopOpacity="0.25" />
                        <stop offset="100%" stopColor="#2170e4" stopOpacity="0.0" />
                      </linearGradient>
                    </defs>
                    
                    {(() => {
                      const maxVal = Math.max(...trends.chart_data.map(d => d.value), 1);
                      const minVal = Math.min(...trends.chart_data.map(d => d.value), 0);
                      const range = maxVal - minVal || 1;
                      
                      const points = trends.chart_data.map((d, i) => {
                        const x = (i / (trends.chart_data.length - 1)) * 100;
                        const y = 45 - ((d.value - minVal) / range) * 38;
                        return `${x},${y}`;
                      }).join(' ');

                      const areaPoints = `0,50 ${points} 100,50`;
                      
                      return (
                        <>
                          <polygon points={areaPoints} fill="url(#chartGradient)" />
                          <polyline points={points} fill="none" stroke="#2170e4" strokeWidth="2.5" strokeLinecap="round" />
                        </>
                      );
                    })()}
                  </svg>
                </div>
                {/* X Axis Labels */}
                <div className="flex justify-between text-[10px] text-on-surface-variant font-mono font-bold mt-2 border-t border-outline-variant/30 pt-1">
                  <span>{trends.chart_data[0].date}</span>
                  <span>{trends.chart_data[Math.floor(trends.chart_data.length / 2)].date}</span>
                  <span>{trends.chart_data[trends.chart_data.length - 1].date}</span>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col justify-center items-center text-center text-on-surface-variant bg-surface-container-low/30 rounded-lg">
                <Info size={24} className="mb-2" />
                <span className="text-sm font-semibold">No date fields found to chart trends.</span>
              </div>
            )}
          </Card>

          {/* Anomaly Alerts List */}
          <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col h-80 text-left hover:shadow-sm transition-shadow">
            <div className="flex justify-between items-center mb-stack-md">
              <h4 className="font-label-md text-label-md text-on-surface m-0 font-bold">Statistical Anomalies</h4>
              <Badge className="bg-orange-50 text-orange-700 border border-orange-100 font-semibold px-2 py-0.5 rounded text-xs">
                {anomalies.anomalies_count} Flagged
              </Badge>
            </div>
            
            {anomalies.anomalies_count > 0 ? (
              <div className="flex-1 overflow-y-auto space-y-2.5 pr-2">
                {anomalies.anomalies.map((anom, idx) => (
                  <div key={idx} className="flex gap-2 items-start text-xs border border-outline-variant/30 p-2 rounded-lg bg-surface-container-low/30 hover:bg-surface-container-low transition-colors">
                    <AlertTriangle className={anom.type === "spike" ? "text-orange-500 mt-0.5 shrink-0" : "text-blue-500 mt-0.5 shrink-0"} size={14} />
                    <div>
                      <span className="font-bold text-slate-800 block mb-0.5">{anom.column_name} (Row {anom.row_index})</span>
                      <span className="text-on-surface-variant leading-relaxed block">{anom.description}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex-1 flex flex-col justify-center items-center text-center text-on-surface-variant bg-surface-container-low/30 rounded-lg">
                <Check size={24} className="text-emerald-500 mb-2" />
                <span className="text-sm font-semibold">No anomalies or spikes detected. Data variance is consistent.</span>
              </div>
            )}
          </Card>

          {/* Correlation Grid (New Card) */}
          <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col h-72 text-left hover:shadow-sm transition-shadow lg:col-span-2">
            <div className="flex justify-between items-center mb-stack-md">
              <h4 className="font-label-md text-label-md text-on-surface m-0 font-bold">Calculated Metric Correlations (Pearson)</h4>
              <Badge className="bg-secondary/10 text-secondary border border-secondary/15 font-semibold px-2 py-0.5 rounded text-xs">
                Significant Relationships
              </Badge>
            </div>
            
            {correlations.correlations.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-stack-md overflow-y-auto pr-1">
                {correlations.correlations.map((corr, idx) => (
                  <div key={idx} className="flex gap-2.5 items-start text-xs border border-outline-variant/30 p-3 rounded-lg bg-surface-container-low/30">
                    <Activity className="text-secondary mt-0.5 shrink-0" size={16} />
                    <div>
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-bold text-slate-800 truncate mr-2">{corr.column_a} ↔ {corr.column_b}</span>
                        <Badge className="bg-primary/5 text-primary text-[10px] font-bold px-1.5 py-0.5 rounded">
                          {corr.coefficient > 0 ? "+" : ""}{corr.coefficient}
                        </Badge>
                      </div>
                      <span className="text-on-surface-variant leading-relaxed block">{corr.description}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex-1 flex flex-col justify-center items-center text-center text-on-surface-variant bg-surface-container-low/30 rounded-lg">
                <Info size={24} className="mb-2" />
                <span className="text-sm font-semibold">No significant correlation coefficients (r &gt;= 0.3) mapped between variables.</span>
              </div>
            )}
          </Card>
        </div>
      </section>

      {/* SECTION 4: Prioritized Recommendations */}
      <section className="space-y-4">
        <h3 className="font-headline-md text-headline-md text-on-surface m-0 font-bold">Actionable Recommendations</h3>
        <Card className="bg-surface rounded-lg card-border overflow-hidden">
          <div className="p-gutter border-b border-outline-variant/50 flex items-center gap-2 bg-surface-container-low text-left">
            <Brain className="text-secondary" size={20} />
            <h2 className="font-headline-md text-headline-md text-on-surface m-0 font-bold">Rule-Based Business Advisory</h2>
          </div>
          <div className="flex flex-col divide-y divide-outline-variant/30 text-left">
            {recommendations.length > 0 ? (
              recommendations.map((rec, idx) => {
                const priorityColor = rec.priority === 'HIGH' ? 'bg-red-100 text-red-700 border border-red-200' :
                                      rec.priority === 'MEDIUM' ? 'bg-amber-100 text-amber-700 border border-amber-200' :
                                      'bg-blue-100 text-blue-700 border border-blue-200';
                return (
                  <div key={idx} className="p-gutter flex flex-col md:flex-row gap-stack-md items-start hover:bg-slate-50/40 transition-colors">
                    <div className="w-full md:w-32 shrink-0">
                      <Badge className={`inline-block px-2.5 py-1 rounded font-bold text-xs uppercase tracking-tight ${priorityColor}`}>
                        {rec.priority} Priority
                      </Badge>
                    </div>
                    <div className="flex-1">
                      <h4 className="font-label-md text-label-md text-on-surface mb-1 font-bold">{rec.recommendation}</h4>
                      <p className="font-body-sm text-body-sm text-on-surface-variant block m-0 leading-relaxed font-medium">
                        {rec.reason}
                      </p>
                    </div>
                    <div className="flex flex-col gap-1 w-full md:w-48 shrink-0 border-l border-outline-variant/30 pl-0 md:pl-4 text-xs">
                      <div className="flex justify-between font-medium">
                        <span className="text-on-surface-variant font-bold">Category:</span>
                        <span className="text-slate-800 font-bold">{rec.category}</span>
                      </div>
                      <div className="flex justify-between font-medium">
                        <span className="text-on-surface-variant font-bold">System Rule:</span>
                        <span className="text-secondary font-bold">Deterministic Match</span>
                      </div>
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="p-gutter text-center text-on-surface-variant font-medium">
                No rule conditions met. Baseline metrics are fully compliant.
              </div>
            )}
          </div>
        </Card>
      </section>
    </main>
  );
}
