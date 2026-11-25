import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { StudioResponse, StudioConfig, ColumnMeta, DatasetStatus } from '../types';
import { DynamicChart } from '../components/DynamicChart';
import { LoadingState, ErrorState, EmptyState } from '../components/StatusStates';
import {
  Palette,
  Play,
  Save,
  Download,
  Filter,
  Plus,
  Trash2,
  Bookmark,
  Layers,
  Sparkles,
  AlertCircle
} from 'lucide-react';

const FALLBACK_COLUMNS: ColumnMeta[] = [
  { name: 'event_type', type: 'character', missing_count: 0, missing_pct: 0, sample_values: ['home', 'product_view', 'add_to_cart'] },
  { name: 'purchase_amount', type: 'numeric', missing_count: 0, missing_pct: 0, sample_values: ['49.99', '120.00'] },
  { name: 'product_category', type: 'character', missing_count: 0, missing_pct: 0, sample_values: ['Electronics', 'Fashion'] },
  { name: 'device_type', type: 'character', missing_count: 0, missing_pct: 0, sample_values: ['desktop', 'mobile', 'tablet'] },
  { name: 'traffic_source', type: 'character', missing_count: 0, missing_pct: 0, sample_values: ['organic', 'paid_search', 'direct'] },
  { name: 'visitor_type', type: 'character', missing_count: 0, missing_pct: 0, sample_values: ['new_visitor', 'returning_visitor'] },
  { name: 'browser', type: 'character', missing_count: 0, missing_pct: 0, sample_values: ['Chrome', 'Safari', 'Firefox'] },
  { name: 'country', type: 'character', missing_count: 0, missing_pct: 0, sample_values: ['United States', 'United Kingdom'] },
  { name: 'session_page_number', type: 'integer', missing_count: 0, missing_pct: 0, sample_values: ['1', '2', '3'] },
  { name: 'time_on_page_seconds', type: 'numeric', missing_count: 0, missing_pct: 0, sample_values: ['45', '120'] },
  { name: 'cart_value', type: 'numeric', missing_count: 0, missing_pct: 0, sample_values: ['0', '85.50'] },
  { name: 'session_converted', type: 'integer', missing_count: 0, missing_pct: 0, sample_values: ['0', '1'] },
  { name: 'customer_segment', type: 'character', missing_count: 0, missing_pct: 0, sample_values: ['Champions', 'At Risk'] },
  { name: 'customer_lifetime_value', type: 'numeric', missing_count: 0, missing_pct: 0, sample_values: ['350.00', '1200.00'] },
  { name: 'previous_purchase_count', type: 'integer', missing_count: 0, missing_pct: 0, sample_values: ['2', '7'] },
  { name: 'discount_percent', type: 'numeric', missing_count: 0, missing_pct: 0, sample_values: ['0', '15'] },
  { name: 'campaign_type', type: 'character', missing_count: 0, missing_pct: 0, sample_values: ['Summer Sale', 'Black Friday'] }
];

export const VisualAnalyticsStudio: React.FC<{
  isDark: boolean;
  onLoadDefault: () => void;
  datasetStatus?: DatasetStatus | null;
}> = ({ isDark, onLoadDefault, datasetStatus }) => {
  const [columns, setColumns] = useState<ColumnMeta[]>(FALLBACK_COLUMNS);
  const [chartType, setChartType] = useState('bar');
  const [xCol, setXCol] = useState('event_type');
  const [yCol, setYCol] = useState('purchase_amount');
  const [groupCol, setGroupCol] = useState('');
  const [aggFunc, setAggFunc] = useState('sum');
  const [sortOrder, setSortOrder] = useState('desc');
  const [limit, setLimit] = useState(25);
  const [filters, setFilters] = useState<{ column: string; operator: string; value: string }[]>([]);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<StudioResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [savedConfigs, setSavedConfigs] = useState<any[]>([]);
  const [configName, setConfigName] = useState('');
  const [saveSuccess, setSaveSuccess] = useState(false);

  const hasDataset = Boolean(datasetStatus?.active_file);

  // Fetch columns and saved configs on mount or when active_file changes
  useEffect(() => {
    const init = async () => {
      try {
        const insp = await api.post('/r/dataset/inspect', {});
        if (insp.data && insp.data.columns && insp.data.columns.length > 0) {
          setColumns(insp.data.columns);
          const cols: string[] = insp.data.columns.map((c: any) => c.name);
          if (cols.includes('event_type')) setXCol('event_type');
          if (cols.includes('purchase_amount')) setYCol('purchase_amount');
        }
        const cfgs = await api.get('/r/studio/configs');
        setSavedConfigs(cfgs.data || []);
      } catch (err: any) {
        // Dataset not yet loaded or inspection in progress
      }
    };
    init();
  }, [datasetStatus?.active_file]);

  const runQuery = async () => {
    if (!hasDataset) {
      setError('Dataset is not uploaded. Please upload a dataset or click "Load Capstone Dataset" to query visualizations.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const resp = await api.post('/r/studio/query', {
        config: {
          chart_type: chartType,
          x_col: xCol,
          y_col: yCol || undefined,
          group_col: groupCol || undefined,
          agg_func: aggFunc,
          filters: filters.filter((f) => f.column && f.value),
          sort_order: sortOrder,
          limit: limit,
        },
      });
      if (resp.data.status === 'error') {
        setError(resp.data.message || 'Error executing query in R');
      } else {
        setResult(resp.data);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to execute query in R service');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (hasDataset) {
      runQuery();
    }
  }, [hasDataset, datasetStatus?.active_file]);

  const handleAddFilter = () => {
    if (columns.length > 0) {
      setFilters([...filters, { column: columns[0].name, operator: '=', value: '' }]);
    }
  };

  const handleRemoveFilter = (index: number) => {
    setFilters(filters.filter((_, i) => i !== index));
  };

  const handleUpdateFilter = (index: number, key: string, val: string) => {
    const updated = [...filters];
    updated[index] = { ...updated[index], [key]: val };
    setFilters(updated);
  };

  const handleSaveConfig = async () => {
    if (!configName) return;
    try {
      const cfgObj = {
        name: configName,
        chart_type: chartType,
        x_col: xCol,
        y_col: yCol,
        group_col: groupCol,
        agg_func: aggFunc,
        filters: filters,
        sort_order: sortOrder,
        limit: limit,
      };
      await api.post('/r/studio/save-config', { config: cfgObj });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
      setConfigName('');
      const cfgs = await api.get('/r/studio/configs');
      setSavedConfigs(cfgs.data || []);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleLoadConfig = (cfg: any) => {
    if (cfg.chart_type) setChartType(cfg.chart_type);
    if (cfg.x_col) setXCol(cfg.x_col);
    if (cfg.y_col !== undefined) setYCol(cfg.y_col);
    if (cfg.group_col !== undefined) setGroupCol(cfg.group_col);
    if (cfg.agg_func) setAggFunc(cfg.agg_func);
    if (cfg.filters) setFilters(cfg.filters);
    if (cfg.sort_order) setSortOrder(cfg.sort_order);
    if (cfg.limit) setLimit(cfg.limit);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            Visual Analytics Studio (Interactive DynamicChart)
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Build custom visualizations: pick dimensions, metrics, aggregations & filters. R computes aggregation and returns ECharts options.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          {result?.echarts_option && (
            <a
              href="http://localhost:8000/api/export/csv?file_type=studio_export"
              download="dynamic_chart_export.csv"
              className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export Aggregated CSV</span>
            </a>
          )}
        </div>
      </div>

      {!hasDataset && (
        <div className="p-4 rounded-xl border border-amber-200 dark:border-amber-800/60 bg-amber-50/70 dark:bg-amber-950/30 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0" />
            <div>
              <p className="text-xs font-semibold text-amber-800 dark:text-amber-200">
                Dataset Not Uploaded
              </p>
              <p className="text-[11px] text-amber-700 dark:text-amber-400">
                Configure your chart dimensions below, then click "Load Capstone Dataset" to render real analytics from R.
              </p>
            </div>
          </div>
          <button
            onClick={onLoadDefault}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-xs transition-colors shrink-0"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Load Capstone Dataset</span>
          </button>
        </div>
      )}

      {error && <ErrorState message={error} onRetry={runQuery} />}

      {/* Query Builder Control Panel */}
      <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 flex items-center">
            <Palette className="w-4 h-4 mr-2 text-blue-600" />
            Visualization Configuration Builder
          </h3>
          <button
            onClick={runQuery}
            disabled={loading}
            className="flex items-center space-x-1.5 px-4 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>{loading ? 'Executing in R...' : 'Render Chart'}</span>
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-xs">
          {/* Chart Type */}
          <div>
            <label className="text-slate-500 dark:text-slate-400 font-medium block mb-1">Chart Type</label>
            <select
              value={chartType}
              onChange={(e) => setChartType(e.target.value)}
              className="w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1.5 text-slate-900 dark:text-slate-100 outline-hidden font-medium"
            >
              <option value="bar">Bar Chart</option>
              <option value="grouped">Grouped Bar</option>
              <option value="stacked">Stacked Bar</option>
              <option value="line">Line Chart</option>
              <option value="area">Area Chart</option>
              <option value="pie">Pie Chart</option>
              <option value="doughnut">Doughnut Chart</option>
              <option value="scatter">Scatter Plot</option>
              <option value="funnel">Funnel</option>
              <option value="treemap">Treemap</option>
              <option value="radar">Radar Chart</option>
            </select>
          </div>

          {/* X Axis */}
          <div>
            <label className="text-slate-600 dark:text-slate-300 font-medium block mb-1">X-Axis / Category</label>
            <select
              value={xCol}
              onChange={(e) => setXCol(e.target.value)}
              className="w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1.5 text-slate-900 dark:text-slate-100 outline-hidden font-medium"
            >
              {columns.map((c) => (
                <option key={c.name} value={c.name}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          {/* Aggregation Function */}
          <div>
            <label className="text-slate-600 dark:text-slate-300 font-medium block mb-1">Aggregation</label>
            <select
              value={aggFunc}
              onChange={(e) => setAggFunc(e.target.value)}
              className="w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1.5 text-slate-900 dark:text-slate-100 outline-hidden font-medium"
            >
              <option value="count">Count (Frequency)</option>
              <option value="sum">Sum</option>
              <option value="mean">Mean (Average)</option>
              <option value="distinct_count">Distinct Count</option>
              <option value="min">Minimum</option>
              <option value="max">Maximum</option>
              <option value="median">Median</option>
            </select>
          </div>

          {/* Y Axis (Metric) */}
          <div>
            <label className="text-slate-600 dark:text-slate-300 font-medium block mb-1">Y-Axis / Metric</label>
            <select
              value={yCol}
              onChange={(e) => setYCol(e.target.value)}
              disabled={aggFunc === 'count'}
              className="w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1.5 text-slate-900 dark:text-slate-100 outline-hidden font-medium disabled:opacity-50"
            >
              <option value="">-- None (Count Rows) --</option>
              {columns.map((c) => (
                <option key={c.name} value={c.name}>
                  {c.name} ({c.type})
                </option>
              ))}
            </select>
          </div>

          {/* Group / Color Dimension */}
          <div>
            <label className="text-slate-600 dark:text-slate-300 font-medium block mb-1">Group By / Series</label>
            <select
              value={groupCol}
              onChange={(e) => setGroupCol(e.target.value)}
              className="w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1.5 text-slate-900 dark:text-slate-100 outline-hidden font-medium"
            >
              <option value="">-- None (Single Series) --</option>
              {columns.map((c) => (
                <option key={c.name} value={c.name}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          {/* Limit */}
          <div>
            <label className="text-slate-600 dark:text-slate-300 font-medium block mb-1">Limit Categories</label>
            <select
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1.5 text-slate-900 dark:text-slate-100 outline-hidden font-medium"
            >
              <option value={10}>Top 10</option>
              <option value={20}>Top 20</option>
              <option value={30}>Top 30</option>
              <option value={50}>Top 50</option>
            </select>
          </div>
        </div>

        {/* Dynamic Filters Section */}
        <div className="pt-3 border-t border-slate-200 dark:border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center">
              <Filter className="w-3.5 h-3.5 mr-1 text-slate-400" />
              Active SQL/data.table Query Filters
            </span>
            <button
              onClick={handleAddFilter}
              className="flex items-center space-x-1 text-xs text-blue-600 hover:text-blue-700 font-medium"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add Filter Condition</span>
            </button>
          </div>

          {filters.length === 0 ? (
            <p className="text-[11px] text-slate-400 italic">No filters applied. Entire dataset will be queried.</p>
          ) : (
            <div className="space-y-2">
              {filters.map((f, idx) => (
                <div key={idx} className="flex items-center space-x-2 text-xs">
                  <select
                    value={f.column}
                    onChange={(e) => handleUpdateFilter(idx, 'column', e.target.value)}
                    className="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2 py-1 text-slate-900 dark:text-slate-100"
                  >
                    {columns.map((c) => (
                      <option key={c.name} value={c.name}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                  <select
                    value={f.operator}
                    onChange={(e) => handleUpdateFilter(idx, 'operator', e.target.value)}
                    className="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2 py-1 text-slate-900 dark:text-slate-100"
                  >
                    <option value="=">=</option>
                    <option value="!=">!=</option>
                    <option value=">">&gt;</option>
                    <option value="<">&lt;</option>
                    <option value=">=">&gt;=</option>
                    <option value="<=">&lt;=</option>
                    <option value="contains">contains</option>
                  </select>
                  <input
                    type="text"
                    placeholder="Filter value..."
                    value={f.value}
                    onChange={(e) => handleUpdateFilter(idx, 'value', e.target.value)}
                    className="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2 py-1 text-slate-900 dark:text-slate-100 flex-1 max-w-xs"
                  />
                  <button
                    onClick={() => handleRemoveFilter(idx)}
                    className="p-1 text-rose-500 hover:text-rose-700"
                    title="Remove filter"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Save Configuration Row */}
        <div className="pt-3 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-2">
            <input
              type="text"
              placeholder="Name this view (e.g., AOV by Device)..."
              value={configName}
              onChange={(e) => setConfigName(e.target.value)}
              className="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1 text-slate-900 dark:text-slate-100 w-64"
            />
            <button
              onClick={handleSaveConfig}
              disabled={!configName}
              className="flex items-center space-x-1 px-3 py-1 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 rounded text-slate-700 dark:text-slate-200 font-medium disabled:opacity-50"
            >
              <Save className="w-3.5 h-3.5" />
              <span>Save View Config</span>
            </button>
            {saveSuccess && <span className="text-emerald-600 font-medium">Saved to session!</span>}
          </div>

          {/* Saved configs pills */}
          {savedConfigs.length > 0 && (
            <div className="flex items-center space-x-1.5 overflow-x-auto max-w-md">
              <span className="text-slate-400 shrink-0">Saved:</span>
              {savedConfigs.map((cfg, idx) => (
                <button
                  key={idx}
                  onClick={() => handleLoadConfig(cfg)}
                  className="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 text-[11px] font-medium border border-blue-200 dark:border-blue-800 hover:bg-blue-100 dark:hover:bg-blue-900 shrink-0"
                >
                  {cfg.name || `View ${idx + 1}`}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {loading && <LoadingState message="R is filtering, aggregating and formatting ECharts option..." />}

      {/* Render Chart */}
      {result?.echarts_option && (
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 capitalize">
                {result.aggregation} of {result.y_column || 'Rows'} by {result.x_column}
              </h3>
              <span className="text-xs text-slate-400">
                {result.total_aggregated_rows} aggregated rows returned from R
              </span>
            </div>
          </div>
          <DynamicChart option={result.echarts_option} height={420} isDark={isDark} />
        </div>
      )}
    </div>
  );
};
