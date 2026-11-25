// TypeScript types for the Capstone Web App

export interface DatasetStatus {
  raw_uploaded: boolean;
  cleaned_available: boolean;
  active_file: string | null;
}

export interface HealthResponse {
  status: string;
  session_id: string;
  r_service: {
    status: string;
    url: string;
    info: Record<string, any>;
  };
  dataset_status: DatasetStatus;
}

export interface ColumnMeta {
  name: string;
  type: string;
  missing_count: number;
  missing_pct: number;
  sample_values: string[];
}

export interface DatasetInspectResponse {
  status: string;
  active_type: string;
  filename: string;
  total_rows: number;
  total_columns: number;
  columns: ColumnMeta[];
  preview: Record<string, any>[];
  duplicate_count_est: number;
  standard_fields: string[];
  auto_mapping: Record<string, string>;
  saved_mapping: Record<string, string>;
}

export interface PreprocessingSummary {
  initial_rows: number;
  final_rows: number;
  rows_removed: number;
  duplicates_removed: number;
  initial_missing: number;
  final_missing: number;
  imputed_values: number;
  outliers_handled: number;
}

export interface PreprocessingResponse {
  status: string;
  message: string;
  summary: PreprocessingSummary;
}

export interface OverviewKPIs {
  dataset_status: string;
  total_events: number;
  total_sessions: number;
  total_customers: number;
  converted_sessions: number;
  conversion_rate: number;
  total_revenue: number;
  avg_order_value: number;
  event_breakdown: { name: string; count: number }[];
  device_breakdown: { name: string; events: number; sessions: number }[];
  traffic_breakdown: { name: string; events: number; sessions: number }[];
  daily_trend: { date: string; events: number; sessions: number; revenue: number }[];
}

export interface NumericStat {
  column: string;
  count: number;
  mean: number;
  std_dev: number;
  min: number;
  q25: number;
  median: number;
  q75: number;
  max: number;
  missing: number;
}

export interface EDAResponse {
  numeric_stats: NumericStat[];
  distributions: {
    column: string;
    bins: string[];
    counts: number[];
  }[];
  correlations: {
    columns: string[];
    items: { x: string; y: string; x_idx: number; y_idx: number; value: number }[];
  };
  categoricals: Record<string, { name: string; count: number }[]>;
  device_conversion: { device: string; sessions: number; conversions: number; rate: number }[];
  traffic_conversion: { source: string; sessions: number; conversions: number; rate: number }[];
}

export interface ClickstreamResponse {
  events: { event_type: string; count: number; sessions: number; avg_time_sec: number }[];
  pages: { page_url: string; views: number; unique_sessions: number; avg_time: number }[];
  top_paths: { path: string; count: number; pct: number }[];
  transitions: {
    events: string[];
    links: { source: string; target: string; count: number; probability: number }[];
  };
  engagement: {
    bounce_count: number;
    bounce_rate: number;
    avg_events_per_session: number;
  };
}

export interface PurchasePatternsResponse {
  categories: { category: string; views: number; purchases: number; revenue: number; conversion_ratio: number }[];
  products: { product: string; views: number; purchases: number; revenue: number }[];
  aov_by_device: { dimension: string; orders: number; revenue: number; aov: number }[];
  aov_by_traffic: { dimension: string; orders: number; revenue: number; aov: number }[];
  hourly: { hour: number; orders: number; revenue: number }[];
  day_of_week: { day: string; orders: number; revenue: number }[];
}

export interface FunnelStage {
  step: number;
  name: string;
  events: string[];
  sessions: number;
  drop_off_count: number;
  drop_off_rate: number;
  step_conversion: number;
  overall_conversion: number;
}

export interface FunnelResponse {
  total_entry_sessions: number;
  overall_funnel_rate: number;
  stages: FunnelStage[];
  available_events: string[];
}

export interface SegmentationResponse {
  selected_k: number;
  silhouette_analysis: { k: number; score: number }[];
  segments_summary: {
    cluster: number;
    segment_name: string;
    customers: number;
    pct_customers: number;
    avg_recency_days: number;
    avg_frequency: number;
    avg_monetary: number;
    total_revenue: number;
  }[];
  scatter_data: {
    id: string;
    pc1: number;
    pc2: number;
    recency: number;
    frequency: number;
    monetary: number;
    segment: string;
    cluster: number;
  }[];
  exact_rules: { segment: string; condition: string }[];
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  auc: number;
  confusion_matrix: { tp: number; tn: number; fp: number; fn: number };
  roc_curve: { fpr: number; tpr: number }[];
}

export interface ConversionPredictionResponse {
  cohort_summary: {
    total_cohort_sessions: number;
    train_sessions: number;
    test_sessions: number;
    cohort_conversion_rate: number;
    majority_class_baseline_accuracy: number;
  };
  models: { name: string; metrics: ModelMetrics }[];
  best_model: string;
  feature_importance: { feature: string; importance: number }[];
}

export interface RegMetrics {
  rmse: number;
  mae: number;
  r_squared: number;
}

export interface RevenueEstimationResponse {
  part_a: {
    train_sessions: number;
    test_sessions: number;
    mean_baseline: { rmse: number; mae: number };
    models: { name: string; metrics: RegMetrics }[];
    best_model: string;
    predicted_vs_actual: { actual: number; predicted: number; residual: number }[];
    feature_importance: { feature: string; importance: number }[];
  };
  part_b: {
    total_expected_revenue: number;
    total_actual_revenue: number;
    by_device: { device: string; actual: number; expected: number }[];
    by_traffic: { traffic: string; actual: number; expected: number }[];
  };
  part_c: {
    forecast_days: number;
    daily_forecast: {
      date: string;
      forecast: number;
      lower_80: number;
      upper_80: number;
      lower_95: number;
      upper_95: number;
    }[];
  };
}

export interface TimeSeriesResponse {
  metric: string;
  interval: string;
  total_periods: number;
  historical: {
    period: string;
    events: number;
    sessions: number;
    conversions: number;
    revenue: number;
    conversion_rate: number;
  }[];
  forecast: {
    period: string;
    forecast: number;
    lower_80: number;
    upper_80: number;
    lower_95: number;
    upper_95: number;
  }[];
}

export interface StudioConfig {
  chart_type: string;
  x_col: string;
  y_col?: string;
  group_col?: string;
  agg_func: string;
  filters?: { column: string; operator: string; value: string }[];
  sort_order?: string;
  limit?: number;
  name?: string;
}

export interface StudioResponse {
  status: string;
  chart_type: string;
  echarts_option: Record<string, any>;
  total_aggregated_rows: number;
  x_column: string;
  y_column?: string;
  aggregation: string;
  message?: string;
}
