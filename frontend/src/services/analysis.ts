import { apiFetch } from './api';

export interface AnalysisResultResponse {
  id: number;
  workspace_id: number | null;
  dataset_id: number;
  business_pulse: number;
  health_label: string;
  pulse_breakdown: {
    data_quality: number;
    completeness: number;
    consistency: number;
    business_performance: number;
  };
  kpis: Record<string, any>;
  hero: {
    metric_name: string;
    group_by_column: string;
    hero_name: string;
    hero_value: number;
    zero_name: string;
    zero_value: number;
    reason: string;
  };
  trends: {
    has_trends: boolean;
    trend_direction: 'Upward' | 'Downward' | 'Stable';
    growth_percent: number;
    chart_data: Array<{ date: string; value: number; moving_avg: number }>;
    metric_name: string;
    date_column: string;
    period: string;
  };
  anomalies: {
    anomalies_count: number;
    high_anomalies: number;
    low_anomalies: number;
    anomalies: Array<{
      column_name: string;
      row_index: number;
      value: number;
      z_score: number;
      type: 'spike' | 'drop';
      description: string;
    }>;
  };
  correlations: {
    correlations: Array<{
      column_a: string;
      column_b: string;
      coefficient: number;
      strength: string;
      description: string;
    }>;
  };
  recommendations: Array<{
    priority: 'HIGH' | 'MEDIUM' | 'LOW';
    category: string;
    recommendation: string;
    reason: string;
  }>;
  insights: string[];
  semantic_profile?: {
    domain: string;
    subdomain: string;
    characteristics: string;
    domain_confidence: number;
    entity: string;
    features: Array<{
      name: string;
      semantic_type: string;
      native_type: string;
      confidence: number;
      possible_meaning: string;
    }>;
    relationships: {
      primary_metrics: string[];
      grouping_dimensions: string[];
      time_dimensions: string[];
      potential_targets: string[];
      categorical_dimensions: string[];
      regression_candidates: Array<{ target: string; features: string[] }>;
      classification_candidates: Array<{ target: string; features: string[] }>;
      forecasting_candidates: Array<{ time_column: string; metric_column: string }>;
      clustering_candidates: string[];
      recommendation_candidates: string[];
    };
    ml_readiness: Record<string, { score: number; reasoning: string }>;
    understanding_reasoning: string;
    visualization_intent: Array<{ intent: string; reasoning: string; suggested_columns: string[] }>;
    kpi_suggestions: Array<{ metric_name: string; aggregation_strategy: string; target_column: string; reasoning: string }>;
    dashboard_suggestions: { layout: string; primary_widget: string; secondary_widgets: string[] };
    report_suggestions: string[];
    chat_context: Record<string, any>;
  };
  dataset_domain?: string;
  entity?: string;
  feature_metadata?: Array<any>;
  relationship_metadata?: Record<string, any>;
  ml_readiness?: Record<string, any>;
  chart_suggestions?: Array<any>;
  kpi_suggestions?: Array<any>;
}

/**
 * Triggers backend business analysis calculations on an ingested dataset.
 * @endpoint POST /api/v1/analyze/{datasetId}
 */
export const runDatasetAnalysis = async (
  datasetId: number
): Promise<AnalysisResultResponse> => {
  console.log('[API Request] POST /api/v1/analyze/' + datasetId);
  return apiFetch<AnalysisResultResponse>(`/v1/analyze/${datasetId}`, {
    method: 'POST',
  });
};

/**
 * Retrieves the cached business analysis reports.
 * @endpoint GET /api/v1/analyze/{datasetId}
 */
export const getAnalysisResult = async (
  datasetId: number
): Promise<AnalysisResultResponse> => {
  console.log('[API Request] GET /api/v1/analyze/' + datasetId);
  return apiFetch<AnalysisResultResponse>(`/v1/analyze/${datasetId}`, {
    method: 'GET',
  });
};

