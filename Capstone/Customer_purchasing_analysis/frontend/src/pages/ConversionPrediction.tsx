import React, { useState } from 'react';
import { api } from '../api/client';
import { ConversionPredictionResponse, DatasetStatus } from '../types';
import { DynamicChart } from '../components/DynamicChart';
import { MetricCard } from '../components/MetricCard';
import { LoadingState, ErrorState, EmptyState } from '../components/StatusStates';
import {
  BrainCircuit,
  Play,
  CheckCircle2,
  Download,
  AlertTriangle,
  AlertCircle,
  Award,
  Sparkles
} from 'lucide-react';

export const ConversionPrediction: React.FC<{
  isDark: boolean;
  onLoadDefault: () => void;
  datasetStatus: DatasetStatus | null;
}> = ({ isDark, onLoadDefault, datasetStatus }) => {
  const [data, setData] = useState<ConversionPredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Feature and Cohort toggles strictly per instructions
  const [includeEarlyCheckout, setIncludeEarlyCheckout] = useState(false);
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
      const resp = await api.post('/r/conversion/train', {
        include_early_checkout: includeEarlyCheckout,
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

  // ROC Curve Chart
  const bestModelData = data?.models.find((m) => m.name === data?.best_model) || data?.models[0];
  const rocCurvePoints = bestModelData?.metrics.roc_curve || [];

  const rocChartOption = {
    tooltip: {
      trigger: 'axis',
      formatter: (p: any) => `FPR: ${p[0].data[0]}<br/>TPR (Sensitivity): <b>${p[0].data[1]}</b>`,
    },
    xAxis: { type: 'value', name: 'False Positive Rate (1 - Specificity)', min: 0, max: 1 },
    yAxis: { type: 'value', name: 'True Positive Rate (Recall)', min: 0, max: 1 },
    series: [
      {
        name: 'ROC',
        type: 'line',
        smooth: true,
        data: rocCurvePoints.map((pt) => [pt.fpr, pt.tpr]),
        itemStyle: { color: '#2563eb' },
        areaStyle: { opacity: 0.2, color: '#3b82f6' },
      },
      {
        name: 'Random Chance Baseline',
        type: 'line',
        data: [[0, 0], [1, 1]],
        lineStyle: { type: 'dashed', color: '#94a3b8' },
        symbol: 'none',
      },
    ],
  };

  // Feature Importance Chart
  const featImpOption = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: { type: 'value', name: 'Importance (Gini / Permutation)' },
    yAxis: {
      type: 'category',
      data: (data?.feature_importance || []).map((f) => f.feature).reverse(),
      axisLabel: { width: 140, overflow: 'truncate' },
    },
    series: [
      {
        name: 'Importance',
        type: 'bar',
        data: (data?.feature_importance || []).map((f) => f.importance).reverse(),
        itemStyle: { color: '#0c87eb', borderRadius: [0, 4, 4, 0] },
      },
    ],
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            Conversion Prediction ML Studio (R)
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Session-level classification strictly using pre-add_to_cart browsing actions & 80/20 chronological split.
          </p>
        </div>
        {data && (
          <a
            href="http://localhost:8000/api/export/csv?file_type=predictions"
            download="conversion_predictions.csv"
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition-colors self-start sm:self-auto"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Predictions CSV</span>
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

      {/* Experimental Protocol & Training Configuration Card */}
      <div className="bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs space-y-4">
        <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 flex items-center">
          <BrainCircuit className="w-4 h-4 mr-2 text-blue-600" />
          Strict Leakage Prevention Protocol & Feature Allowlist
        </h3>

        <div className="p-3 bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800 rounded-lg text-xs text-blue-800 dark:text-blue-300">
          <strong>Strict ML Course Rules Enforced:</strong> Target = <code>session_converted</code>. Cut point = first <code>add_to_cart</code> (only events before it). Never uses purchase_amount, is_conversion_event, discount_percent, or post-cart events to prevent fake 99% accuracy. Realistic AUC expectation: 0.60 – 0.75.
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          {/* Customer Attributes Toggle */}
          <label className="flex items-start space-x-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input
              type="checkbox"
              checked={includeCustomerAttr}
              onChange={(e) => setIncludeCustomerAttr(e.target.checked)}
              className="mt-1 rounded text-blue-600 focus:ring-blue-500"
            />
            <div>
              <span className="text-xs font-semibold text-slate-800 dark:text-slate-200 block">
                Include Customer Historical Attributes
              </span>
              <span className="text-[11px] text-slate-500 dark:text-slate-400">
                Adds CLV, historical average order value, previous purchase count, loyalty status, tenure days.
              </span>
            </div>
          </label>

          {/* Early Checkout Cohort Toggle */}
          <label className="flex items-start space-x-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 cursor-pointer">
            <input
              type="checkbox"
              checked={includeEarlyCheckout}
              onChange={(e) => setIncludeEarlyCheckout(e.target.checked)}
              className="mt-1 rounded text-blue-600 focus:ring-blue-500"
            />
            <div>
              <span className="text-xs font-semibold text-slate-800 dark:text-slate-200 block">
                Include Early Checkout Sessions
              </span>
              <span className="text-[11px] text-amber-600 dark:text-amber-400">
                Warning: Sessions with checkout before cart represent data artifacts that almost always convert.
              </span>
            </div>
          </label>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-slate-200 dark:border-slate-800">
          <span className="text-xs text-slate-400 font-mono">
            Models: glm (logit), rpart, randomForest (100 trees), xgboost
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
                ? 'Training 4 Models in R...'
                : hasDataset
                ? 'Train Conversion Models'
                : 'Dataset Not Uploaded (Click to Load)'}
            </span>
          </button>
        </div>
      </div>

      {loading && <LoadingState message="Training Logistic Regression, Decision Tree, Random Forest & XGBoost in R..." />}

      {!loading && !data && hasDataset && (
        <EmptyState
          title="Ready to Train Conversion Classifiers"
          description="Click 'Train Conversion Models' to build, validate, and compare models on the held-out test cohort."
          onAction={handleTrain}
          actionText="Train Models Now"
        />
      )}

      {/* Results Section */}
      {data && (
        <>
          {/* Cohort Summary KPIs */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <span className="text-xs text-slate-400 uppercase font-semibold">Add-to-Cart Cohort</span>
              <p className="text-2xl font-bold text-slate-800 dark:text-slate-100 mt-1">
                {data.cohort_summary.total_cohort_sessions.toLocaleString()}
              </p>
              <span className="text-[11px] text-slate-400">Sessions reaching cart</span>
            </div>
            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <span className="text-xs text-slate-400 uppercase font-semibold">Chronological Split</span>
              <p className="text-2xl font-bold text-slate-800 dark:text-slate-100 mt-1">
                {data.cohort_summary.train_sessions} / {data.cohort_summary.test_sessions}
              </p>
              <span className="text-[11px] text-blue-600 dark:text-blue-400">80% Train / 20% Test</span>
            </div>
            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <span className="text-xs text-slate-400 uppercase font-semibold">Cohort Conv Rate</span>
              <p className="text-2xl font-bold text-slate-800 dark:text-slate-100 mt-1">
                {data.cohort_summary.cohort_conversion_rate}%
              </p>
              <span className="text-[11px] text-emerald-600">Actual cart-to-buy rate</span>
            </div>
            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <span className="text-xs text-slate-400 uppercase font-semibold">Majority Baseline Acc</span>
              <p className="text-2xl font-bold text-slate-800 dark:text-slate-100 mt-1">
                {(data.cohort_summary.majority_class_baseline_accuracy * 100).toFixed(1)}%
              </p>
              <span className="text-[11px] text-slate-400">Zero-rule baseline</span>
            </div>
          </div>

          {/* Model Comparison Table */}
          <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 flex items-center">
                <Award className="w-4 h-4 mr-2 text-amber-500" />
                Model Benchmark & Performance Comparison (Held-Out Test Set)
              </h3>
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400 border border-amber-200 dark:border-amber-800">
                Best Model: {data.best_model}
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-xs font-mono">
                <thead className="bg-slate-50 dark:bg-slate-800/60">
                  <tr>
                    <th className="px-3 py-2 text-left font-semibold text-slate-700 dark:text-slate-300">Model Algorithm</th>
                    <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Accuracy</th>
                    <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Precision</th>
                    <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Recall</th>
                    <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">F1-Score</th>
                    <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">ROC-AUC</th>
                    <th className="px-3 py-2 text-center font-semibold text-slate-700 dark:text-slate-300">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {data.models.map((m) => {
                    const isBest = m.name === data.best_model;
                    return (
                      <tr
                        key={m.name}
                        className={isBest ? 'bg-blue-50/60 dark:bg-blue-950/40 font-bold' : 'hover:bg-slate-50 dark:hover:bg-slate-800/40'}
                      >
                        <td className="px-3 py-2 text-slate-800 dark:text-slate-200">
                          {m.name}
                          {isBest && <span className="ml-2 text-[10px] text-blue-600 uppercase font-extrabold">(Best)</span>}
                        </td>
                        <td className="px-3 py-2 text-right">{(m.metrics.accuracy * 100).toFixed(1)}%</td>
                        <td className="px-3 py-2 text-right">{(m.metrics.precision * 100).toFixed(1)}%</td>
                        <td className="px-3 py-2 text-right">{(m.metrics.recall * 100).toFixed(1)}%</td>
                        <td className="px-3 py-2 text-right">{m.metrics.f1.toFixed(3)}</td>
                        <td className="px-3 py-2 text-right text-blue-600 dark:text-blue-400 font-extrabold">
                          {m.metrics.auc.toFixed(3)}
                        </td>
                        <td className="px-3 py-2 text-center">
                          {isBest ? (
                            <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300 font-bold">
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

          {/* Charts: ROC Curve & Feature Importance */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* ROC Curve */}
            <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                  ROC Curve ({data.best_model} - AUC: {bestModelData?.metrics.auc.toFixed(3)})
                </h3>
                <span className="text-xs text-slate-400">pROC package</span>
              </div>
              <DynamicChart option={rocChartOption} height={320} isDark={isDark} />
            </div>

            {/* Feature Importance */}
            <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                  Feature Importance (Random Forest Gini)
                </h3>
                <span className="text-xs text-slate-400">Pre-cart features</span>
              </div>
              <DynamicChart option={featImpOption} height={320} isDark={isDark} />
            </div>
          </div>
        </>
      )}
    </div>
  );
};
