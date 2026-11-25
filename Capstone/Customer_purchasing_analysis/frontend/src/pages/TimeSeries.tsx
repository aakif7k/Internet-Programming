import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { TimeSeriesResponse } from '../types';
import { DynamicChart } from '../components/DynamicChart';
import { MetricCard } from '../components/MetricCard';
import { LoadingState, ErrorState, EmptyState } from '../components/StatusStates';
import { TrendingUp, Calendar, RefreshCw, Activity } from 'lucide-react';

export const TimeSeries: React.FC<{ isDark: boolean; onLoadDefault: () => void }> = ({
  isDark,
  onLoadDefault,
}) => {
  const [data, setData] = useState<TimeSeriesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [metric, setMetric] = useState('revenue');
  const [interval, setInterval] = useState('daily');
  const [forecastPeriods, setForecastPeriods] = useState(14);

  const fetchTimeSeries = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await api.get('/r/timeseries/analysis', {
        params: { metric, interval, forecast_periods: forecastPeriods },
      });
      setData(resp.data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTimeSeries();
  }, [metric, interval, forecastPeriods]);

  if (loading && !data) return <LoadingState message="Aggregating time-series and fitting forecast model in R..." />;
  if (error) {
    if (error.includes('No dataset uploaded')) {
      return (
        <EmptyState
          title="No Time-Series Data Loaded"
          description="Upload your clickstream dataset to generate time-series forecasts."
          onAction={onLoadDefault}
        />
      );
    }
    return <ErrorState message={error} onRetry={fetchTimeSeries} />;
  }
  if (!data) return null;

  // Chart configuration: Historical points + Forecasted points with confidence bands
  const histPeriods = data.historical.map((h) => h.period);
  const histValues = data.historical.map((h) => {
    if (metric === 'revenue') return h.revenue;
    if (metric === 'sessions') return h.sessions;
    if (metric === 'conversions') return h.conversions;
    return h.conversion_rate;
  });

  const fcPeriods = (data.forecast || []).map((f) => f.period);
  const fcValues = (data.forecast || []).map((f) => f.forecast);
  const fcLower80 = (data.forecast || []).map((f) => f.lower_80);
  const fcUpper80 = (data.forecast || []).map((f) => f.upper_80);
  const fcLower95 = (data.forecast || []).map((f) => f.lower_95);
  const fcUpper95 = (data.forecast || []).map((f) => f.upper_95);

  const allX = [...histPeriods, ...fcPeriods];

  // Align historical series with nulls for forecast periods
  const alignedHist = [...histValues, ...fcPeriods.map(() => null)];
  // Align forecast series with nulls for historical periods (except connecting to last historical point)
  const lastHistVal = histValues[histValues.length - 1];
  const alignedFc = [
    ...histPeriods.slice(0, -1).map(() => null),
    lastHistVal,
    ...fcValues,
  ];

  const alignedUpper80 = [
    ...histPeriods.slice(0, -1).map(() => null),
    lastHistVal,
    ...fcUpper80,
  ];
  const alignedLower80 = [
    ...histPeriods.slice(0, -1).map(() => null),
    lastHistVal,
    ...fcLower80,
  ];

  const tsOption = {
    tooltip: { trigger: 'axis' },
    legend: { top: 0 },
    xAxis: {
      type: 'category',
      data: allX,
      axisLabel: { rotate: 30, interval: 'auto' },
    },
    yAxis: {
      type: 'value',
      name: metric === 'revenue' ? 'Revenue ($)' : metric === 'conversion_rate' ? 'Rate (%)' : 'Count',
    },
    series: [
      {
        name: `Historical (${metric})`,
        type: 'line',
        data: alignedHist,
        itemStyle: { color: '#2563eb' },
        lineStyle: { width: 2 },
      },
      {
        name: `Forecast (${data.forecast.length} periods)`,
        type: 'line',
        data: alignedFc,
        itemStyle: { color: '#10b981' },
        lineStyle: { width: 2, type: 'dashed' },
      },
      {
        name: 'Upper 80% Bound',
        type: 'line',
        data: alignedUpper80,
        lineStyle: { opacity: 0 },
        symbol: 'none',
        stack: 'band-80',
      },
      {
        name: 'Lower 80% Bound',
        type: 'line',
        data: alignedLower80,
        lineStyle: { opacity: 0 },
        symbol: 'none',
        areaStyle: { color: '#a7f3d0', opacity: 0.4 },
        stack: 'band-80',
      },
    ],
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            Time-Series Aggregation & ARIMA/ETS Forecasting (R)
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Statistical temporal modeling using R's forecast package with automatic order selection and confidence bounds.
          </p>
        </div>
        <button
          onClick={fetchTimeSeries}
          className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-xs transition-colors self-start sm:self-auto"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Forecast</span>
        </button>
      </div>

      {/* Control Filters Bar */}
      <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs flex flex-wrap items-center gap-4 text-xs">
        <div className="flex items-center space-x-2">
          <span className="font-semibold text-slate-700 dark:text-slate-300">Metric:</span>
          <select
            value={metric}
            onChange={(e) => setMetric(e.target.value)}
            className="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1 text-slate-900 dark:text-slate-100 font-medium outline-hidden"
          >
            <option value="revenue">Total Revenue ($)</option>
            <option value="sessions">Total Sessions</option>
            <option value="conversions">Total Conversions</option>
            <option value="conversion_rate">Conversion Rate (%)</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <span className="font-semibold text-slate-700 dark:text-slate-300">Interval:</span>
          <select
            value={interval}
            onChange={(e) => setInterval(e.target.value)}
            className="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1 text-slate-900 dark:text-slate-100 font-medium outline-hidden"
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <span className="font-semibold text-slate-700 dark:text-slate-300">Forecast Horizon:</span>
          <select
            value={forecastPeriods}
            onChange={(e) => setForecastPeriods(Number(e.target.value))}
            className="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded px-2.5 py-1 text-slate-900 dark:text-slate-100 font-medium outline-hidden"
          >
            <option value={7}>7 Periods Ahead</option>
            <option value={14}>14 Periods Ahead</option>
            <option value={30}>30 Periods Ahead</option>
          </select>
        </div>
      </div>

      {/* Main Forecast Chart */}
      <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 flex items-center">
            <TrendingUp className="w-4 h-4 mr-2 text-blue-600" />
            Time-Series Forecast (forecast::auto.arima) with 80% Confidence Interval
          </h3>
          <span className="text-xs text-slate-400 capitalize">
            {interval} {metric}
          </span>
        </div>
        <DynamicChart option={tsOption} height={380} isDark={isDark} />
      </div>

      {/* Historical Data Table */}
      <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
        <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3">
          Aggregated Time-Series Data Points
        </h3>
        <div className="overflow-x-auto max-h-72 overflow-y-auto">
          <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-xs font-mono">
            <thead className="bg-slate-50 dark:bg-slate-800/60 sticky top-0">
              <tr>
                <th className="px-3 py-2 text-left font-semibold text-slate-700 dark:text-slate-300">Period</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Events</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Sessions</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Conversions</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Conversion Rate</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Revenue ($)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {data.historical.map((row) => (
                <tr key={row.period} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                  <td className="px-3 py-1.5 font-medium text-slate-800 dark:text-slate-200">{row.period}</td>
                  <td className="px-3 py-1.5 text-right text-slate-500">{row.events.toLocaleString()}</td>
                  <td className="px-3 py-1.5 text-right text-slate-500">{row.sessions.toLocaleString()}</td>
                  <td className="px-3 py-1.5 text-right text-slate-500">{row.conversions.toLocaleString()}</td>
                  <td className="px-3 py-1.5 text-right text-blue-600 dark:text-blue-400 font-semibold">{row.conversion_rate}%</td>
                  <td className="px-3 py-1.5 text-right text-emerald-600 dark:text-emerald-400 font-bold">${row.revenue.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
