import React, { useState } from 'react';
import { api } from '../api/client';
import { RevenueEstimationResponse, DatasetStatus } from '../types';
import { DynamicChart } from '../components/DynamicChart';
import { MetricCard } from '../components/MetricCard';
import { LoadingState, ErrorState, EmptyState } from '../components/StatusStates';
import {
  DollarSign,
  Play,
  TrendingUp,
  Download,
  Award,
  AlertCircle,
  Sparkles
} from 'lucide-react';

export const RevenueEstimation: React.FC<{
  isDark: boolean;
  onLoadDefault: () => void;
  datasetStatus: DatasetStatus | null;
}> = ({ isDark, onLoadDefault, datasetStatus }) => {
  const [data, setData] = useState<RevenueEstimationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [includeFirstCartItem, setIncludeFirstCartItem] = useState(true);
  const [includeCustomerAttr, setIncludeCustomerAttr] = useState(true);

  const hasDataset = Boolean(datasetStatus?.active_file);

  const handleTrain = async () => {
    if (!hasDataset) {
      setError('Dataset is not uploaded. Please upload your clickstream dataset or click "Load Capstone Dataset" first.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const resp = await api.post('/r/revenue/train', {
        include_first_cart_item: includeFirstCartItem,
        include_customer_attr: includeCustomerAttr,
      });
      if (resp.data.status === 'error') {
        setError(resp.data.message);
      } else {
        setData(resp.data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Chart 1: Predicted vs Actual Scatter Plot
  const predVsActualOption = {
    tooltip: {
      formatter: (p: any) =>
        `Actual: <b>$${p.data[0]}</b><br/>Predicted: <b>$${p.data[1]}</b><br/>Residual: $${(p.data[0] - p.data[1]).toFixed(2)}`,
    },
    xAxis: { type: 'value', name: 'Actual Order Value ($)' },
    yAxis: { type: 'value', name: 'Predicted Order Value ($)' },
    series: [
      {
        name: 'Order Value',
        type: 'scatter',
        symbolSize: 8,
        data: (data?.part_a.predicted_vs_actual || []).map((pt) => [pt.actual, pt.predicted]),
        itemStyle: { color: '#0c87eb' },
      },
    ],
  };

  // Chart 2: Expected Revenue by Device (Part B)
  const deviceExpectedOption = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { top: 0 },
    xAxis: {
      type: 'category',
      data: (data?.part_b.by_device || []).map((d) => d.device),
    },
    yAxis: { type: 'value', name: 'Revenue ($)' },
    series: [
      {
        name: 'Actual Revenue',
        type: 'bar',
        data: (data?.part_b.by_device || []).map((d) => d.actual),
        itemStyle: { color: '#93c5fd', borderRadius: [4, 4, 0, 0] },
      },
      {
        name: 'Expected Revenue (P(conv) * Order Value)',
        type: 'bar',
        data: (data?.part_b.by_device || []).map((d) => d.expected),
        itemStyle: { color: '#3b82f6', borderRadius: [4, 4, 0, 0] },
      },
    ],
  };

  // Chart 3: 30-Day Revenue Forecast (Part C)
  const forecastDates = (data?.part_c.daily_forecast || []).map((f) => f.date);
  const forecastMean = (data?.part_c.daily_forecast || []).map((f) => f.forecast);
  const forecastLower80 = (data?.part_c.daily_forecast || []).map((f) => f.lower_80);
  const forecastUpper80 = (data?.part_c.daily_forecast || []).map((f) => f.upper_80);

  const forecastChartOption = {
    tooltip: { trigger: 'axis' },
    legend: { top: 0 },
    xAxis: { type: 'category', data: forecastDates, axisLabel: { rotate: 30 } },
    yAxis: { type: 'value', name: 'Forecasted Daily Revenue ($)' },
    series: [
      {
        name: 'Forecast Mean',
        type: 'line',
        smooth: true,
        data: forecastMean,
        itemStyle: { color: '#10b981' },
      },
      {
        name: 'Confidence Interval (80%)',
        type: 'line',
        smooth: true,
        data: forecastUpper80,
        lineStyle: { opacity: 0 },
        stack: 'confidence-band',
        symbol: 'none',
      },
      {
        name: 'Lower 80%',
        type: 'line',
        smooth: true,
        data: forecastLower80,
        lineStyle: { opacity: 0 },
        areaStyle: { color: '#d1fae5', opacity: 0.5 },
        stack: 'confidence-band',
        symbol: 'none',
      },
    ],
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            Revenue Estimation & Expected Monetary Value (R)
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Order value regression, expected revenue calculation (P(convert) &times; Order Value), and 30-day time-series forecast.
          </p>
        </div>
        {data && (
          <a
            href="http://localhost:8000/api/export/csv?file_type=revenue_predictions"
            download="revenue_predictions.csv"
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition-colors self-start sm:self-auto"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Revenue CSV</span>
          </a>
        )}
      </div>

      {/* Dataset not loaded banner */}
      {!hasDataset && (
        <div className="p-4 bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-700 rounded-xl text-amber-900 dark:text-amber-200 text-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0" />
            <div>
              <span className="font-bold">Dataset is not uploaded.</span>
              <p className="text-xs text-amber-700 dark:text-amber-300 mt-0.5">
                Please upload a clickstream CSV or load the sample capstone dataset before training models.
              </p>
            </div>
          </div>
          <button
            onClick={onLoadDefault}
            className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-semibold shrink-0"
          >
            Load Capstone Dataset
          </button>
        </div>
      )}

      {error && <ErrorState message={error} onRetry={handleTrain} />}

      {/* Regression Configuration Card */}
      <div className="bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs space-y-4">
        <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 flex items-center">
          <DollarSign className="w-4 h-4 mr-2 text-emerald-600" />
          Regression Features & Configuration
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label className="flex items-start space-x-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input
              type="checkbox"
              checked={includeFirstCartItem}
              onChange={(e) => setIncludeFirstCartItem(e.target.checked)}
              className="mt-1 rounded text-blue-600 focus:ring-blue-500"
            />
            <div>
              <span className="text-xs font-semibold text-slate-800 dark:text-slate-200 block">
                Include First Cart Item Price & Category
              </span>
              <span className="text-[11px] text-slate-500 dark:text-slate-400">
                Observable at prediction time (first add_to_cart trigger point).
              </span>
            </div>
          </label>

          <label className="flex items-start space-x-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input
              type="checkbox"
              checked={includeCustomerAttr}
              onChange={(e) => setIncludeCustomerAttr(e.target.checked)}
              className="mt-1 rounded text-blue-600 focus:ring-blue-500"
            />
            <div>
              <span className="text-xs font-semibold text-slate-800 dark:text-slate-200 block">
                Include Customer Attributes
              </span>
              <span className="text-[11px] text-slate-500 dark:text-slate-400">
                Customer Lifetime Value (CLV), historical AOV, and purchase count.
              </span>
            </div>
          </label>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-slate-200 dark:border-slate-800">
          <span className="text-xs text-slate-400 font-mono">
            Models: Linear Regression (lm), Random Forest (randomForest), XGBoost (xgboost)
          </span>
          <button
            onClick={handleTrain}
            disabled={loading}
            className={`flex items-center space-x-2 px-5 py-2.5 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors ${
              hasDataset ? 'bg-blue-600 hover:bg-blue-700' : 'bg-slate-400 cursor-not-allowed'
            }`}
          >
            <Play className="w-4 h-4 fill-current" />
            <span>
              {loading
                ? 'Training Revenue Models in R...'
                : hasDataset
                ? 'Train Revenue Models'
                : 'Dataset Not Uploaded (Click to Load)'}
            </span>
          </button>
        </div>
      </div>

      {loading && <LoadingState message="Fitting Linear Regression, Random Forest and XGBoost in R..." />}

      {!loading && !data && hasDataset && (
        <EmptyState
          title="Ready to Estimate Order Values & Revenue"
          description="Click 'Train Revenue Models' to fit order value regressors and compute expected revenue per session."
          onAction={handleTrain}
          actionText="Train Revenue Models Now"
        />
      )}

      {data && (
        <>
          {/* Part A: Regressor Benchmark Table */}
          <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 flex items-center">
                <Award className="w-4 h-4 mr-2 text-amber-500" />
                Part A: Order Value Regressors (Target = Session Purchase Amount)
              </h3>
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-400 border border-blue-200 dark:border-blue-800">
                Best Regressor: {data.part_a.best_model}
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-xs font-mono">
                <thead className="bg-slate-50 dark:bg-slate-800/60">
                  <tr>
                    <th className="px-3 py-2 text-left font-semibold text-slate-700 dark:text-slate-300">Model</th>
                    <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">RMSE ($)</th>
                    <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">MAE ($)</th>
                    <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">R-Squared</th>
                    <th className="px-3 py-2 text-center font-semibold text-slate-700 dark:text-slate-300">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  <tr className="bg-slate-50/50 dark:bg-slate-800/30 text-slate-500">
                    <td className="px-3 py-2">Mean Prediction Baseline</td>
                    <td className="px-3 py-2 text-right">${data.part_a.mean_baseline.rmse}</td>
                    <td className="px-3 py-2 text-right">${data.part_a.mean_baseline.mae}</td>
                    <td className="px-3 py-2 text-right">0.000</td>
                    <td className="px-3 py-2 text-center text-slate-400">Baseline</td>
                  </tr>
                  {data.part_a.models.map((m) => {
                    const isBest = m.name === data.part_a.best_model;
                    return (
                      <tr
                        key={m.name}
                        className={isBest ? 'bg-blue-50/60 dark:bg-blue-950/40 font-bold' : 'hover:bg-slate-50 dark:hover:bg-slate-800/40'}
                      >
                        <td className="px-3 py-2 text-slate-800 dark:text-slate-200">{m.name}</td>
                        <td className="px-3 py-2 text-right text-blue-600 dark:text-blue-400">${m.metrics.rmse}</td>
                        <td className="px-3 py-2 text-right">${m.metrics.mae}</td>
                        <td className="px-3 py-2 text-right">{m.metrics.r_squared}</td>
                        <td className="px-3 py-2 text-center">
                          {isBest ? (
                            <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300">
                              Selected
                            </span>
                          ) : (
                            <span className="text-slate-400 text-[10px]">Evaluated</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Part A Charts: Predicted vs Actual */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
              <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3">
                Predicted vs Actual Order Values (Held-Out Test Set)
              </h3>
              <DynamicChart option={predVsActualOption} height={320} isDark={isDark} />
            </div>

            <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
              <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3">
                Part B: Expected vs Actual Revenue by Device Type
              </h3>
              <DynamicChart option={deviceExpectedOption} height={320} isDark={isDark} />
            </div>
          </div>

          {/* Part C: 30-Day Revenue Forecast with ARIMA */}
          <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                  Part C: 30-Day Daily Revenue Forecast (R forecast package)
                </h3>
                <p className="text-xs text-slate-400">ARIMA / ETS point forecast with 80% confidence interval</p>
              </div>
            </div>
            <DynamicChart option={forecastChartOption} height={320} isDark={isDark} />
          </div>
        </>
      )}
    </div>
  );
};
