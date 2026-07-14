/**
 * AI Analysis and Business Insights API Service Contract for InsightPilot
 * Target Backend: FastAPI
 */

export interface AnalysisRunRequest {
  datasetId: string;
}

export interface PulseMetrics {
  score: number;
  status: 'healthy' | 'warning' | 'critical';
  confidence: number;
  trendPercentage: number;
}

export interface BusinessSignal {
  name: string;
  value: string;
  changePercent: number;
  trend: 'up' | 'down' | 'neutral';
  status: string;
}

export interface AIInsight {
  pulseScore: number;
  topCategory: string;
  underperformingCategory: string;
  primaryInsight: string;
  recommendations: Array<{
    id: string;
    priority: 'high' | 'medium' | 'low';
    title: string;
    description: string;
    impact: string;
    confidence: number;
  }>;
}

/**
 * Triggers backend AI analysis loop on a loaded dataset.
 * @endpoint POST /api/v1/analysis/run
 * @headers X-Session-ID
 */
export const runDatasetAnalysis = async (
  data: AnalysisRunRequest,
  sessionId: string
): Promise<{ success: boolean; taskId: string }> => {
  console.log('[API Request] POST /api/v1/analysis/run', { data, sessionId });
  
  await new Promise((resolve) => setTimeout(resolve, 500));
  
  return {
    success: true,
    taskId: `task_ai_${Math.random().toString(36).substr(2, 9)}`,
  };
};

/**
 * Fetches dashboard Business Pulse metrics.
 * @endpoint GET /api/v1/analysis/pulse
 * @headers X-Session-ID
 */
export const fetchPulseMetrics = async (sessionId: string): Promise<PulseMetrics> => {
  console.log('[API Request] GET /api/v1/analysis/pulse', { sessionId });
  
  await new Promise((resolve) => setTimeout(resolve, 300));
  
  return {
    score: 87,
    status: 'healthy',
    confidence: 92,
    trendPercentage: 4.2,
  };
};

/**
 * Fetches 5-card business signal indicators.
 * @endpoint GET /api/v1/analysis/signals
 * @headers X-Session-ID
 */
export const fetchBusinessSignals = async (sessionId: string): Promise<BusinessSignal[]> => {
  console.log('[API Request] GET /api/v1/analysis/signals', { sessionId });

  await new Promise((resolve) => setTimeout(resolve, 300));

  return [
    { name: 'Revenue', value: '+18%', changePercent: 18, trend: 'up', status: 'Healthy' },
    { name: 'Profit', value: '+6%', changePercent: 6, trend: 'up', status: 'Stable' },
    { name: 'Customer Health', value: '-2.4%', changePercent: -2.4, trend: 'down', status: 'Needs Attention' },
    { name: 'Growth', value: '+11%', changePercent: 11, trend: 'up', status: 'Strong' },
    { name: 'Risk Level', value: 'Medium', changePercent: 0, trend: 'neutral', status: 'Monitoring' },
  ];
};

/**
 * Fetches AI recommendations and performance categories.
 * @endpoint GET /api/v1/analysis/insights
 * @headers X-Session-ID
 */
export const fetchAIInsights = async (sessionId: string): Promise<AIInsight> => {
  console.log('[API Request] GET /api/v1/analysis/insights', { sessionId });

  await new Promise((resolve) => setTimeout(resolve, 400));

  return {
    pulseScore: 87,
    topCategory: 'Electronics',
    underperformingCategory: 'Furniture',
    primaryInsight: 'Revenue grew by 14% this quarter, primarily driven by enterprise contract renewals. Mid-market CAC increased by 8%.',
    recommendations: [
      {
        id: 'rec_1',
        priority: 'high',
        title: 'Improve customer retention campaign',
        description: 'Churn risk detected in mid-market segment. Proactive outreach recommended.',
        impact: 'High',
        confidence: 94,
      },
      {
        id: 'rec_2',
        priority: 'medium',
        title: 'Optimize supply chain logistics',
        description: 'Route inefficiencies identified in APAC region contributing to margin compression.',
        impact: 'Medium',
        confidence: 82,
      }
    ],
  };
};
