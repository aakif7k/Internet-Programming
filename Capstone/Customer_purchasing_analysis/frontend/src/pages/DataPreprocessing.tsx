import React, { useState } from 'react';
import { api } from '../api/client';
import { PreprocessingResponse } from '../types';
import { LoadingState, ErrorState } from '../components/StatusStates';
import {
  SlidersHorizontal,
  Play,
  CheckCircle2,
  Download,
  AlertCircle,
  FileCheck2,
  ArrowRight
} from 'lucide-react';
import { Link } from 'react-router-dom';

export const DataPreprocessing: React.FC<{ onCleanedReady: () => void }> = ({ onCleanedReady }) => {
  const [removeDuplicates, setRemoveDuplicates] = useState(true);
  const [handleMissing, setHandleMissing] = useState('impute');
  const [parseDates, setParseDates] = useState(true);
  const [filterOutliers, setFilterOutliers] = useState(true);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PreprocessingResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRunPreprocessing = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await api.post('/r/preprocessing/run', {
        options: {
          remove_duplicates: removeDuplicates,
          handle_missing: handleMissing,
          parse_dates: parseDates,
          filter_outliers: filterOutliers,
        },
      });
      setResult(resp.data);
      onCleanedReady();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            Data Preprocessing & Cleansing Engine (R)
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Execute automated data cleaning, missing value imputation, timestamp validation, and IQR outlier handling in R.
          </p>
        </div>
        {result && (
          <a
            href="http://localhost:8000/api/export/csv?file_type=cleaned"
            download="cleaned_clickstream.csv"
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Cleaned CSV</span>
          </a>
        )}
      </div>

      {error && <ErrorState message={error} onRetry={handleRunPreprocessing} />}

      {/* Preprocessing Configuration Form */}
      <div className="bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs space-y-6">
        <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 flex items-center">
          <SlidersHorizontal className="w-4 h-4 mr-2 text-blue-600" />
          Data Quality Pipeline Rules
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Rule 1: Duplicate handling */}
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60">
            <label className="flex items-start space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={removeDuplicates}
                onChange={(e) => setRemoveDuplicates(e.target.checked)}
                className="mt-1 rounded text-blue-600 focus:ring-blue-500"
              />
              <div>
                <span className="text-sm font-semibold text-slate-800 dark:text-slate-200 block">
                  Deduplicate Event Records
                </span>
                <span className="text-xs text-slate-500 dark:text-slate-400">
                  Identifies and removes exact duplicate event rows across all dimensions.
                </span>
              </div>
            </label>
          </div>

          {/* Rule 2: Timestamp Parsing */}
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60">
            <label className="flex items-start space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={parseDates}
                onChange={(e) => setParseDates(e.target.checked)}
                className="mt-1 rounded text-blue-600 focus:ring-blue-500"
              />
              <div>
                <span className="text-sm font-semibold text-slate-800 dark:text-slate-200 block">
                  Parse & Standardize Timestamps
                </span>
                <span className="text-xs text-slate-500 dark:text-slate-400">
                  Converts ISO/custom event timestamps to standard UTC POSIXct representation.
                </span>
              </div>
            </label>
          </div>

          {/* Rule 3: Missing Value Handling */}
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60">
            <span className="text-sm font-semibold text-slate-800 dark:text-slate-200 block mb-2">
              Missing Value Strategy
            </span>
            <div className="space-y-2">
              <label className="flex items-center space-x-2 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
                <input
                  type="radio"
                  name="missing_strategy"
                  value="impute"
                  checked={handleMissing === 'impute'}
                  onChange={(e) => setHandleMissing(e.target.value)}
                  className="text-blue-600 focus:ring-blue-500"
                />
                <span>Impute (Numeric: Median, Categorical: "Unknown" / Mode)</span>
              </label>
              <label className="flex items-center space-x-2 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
                <input
                  type="radio"
                  name="missing_strategy"
                  value="drop"
                  checked={handleMissing === 'drop'}
                  onChange={(e) => setHandleMissing(e.target.value)}
                  className="text-blue-600 focus:ring-blue-500"
                />
                <span>Drop rows with missing key identifiers (session_id, customer_id)</span>
              </label>
            </div>
          </div>

          {/* Rule 4: Outlier Treatment */}
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60">
            <label className="flex items-start space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={filterOutliers}
                onChange={(e) => setFilterOutliers(e.target.checked)}
                className="mt-1 rounded text-blue-600 focus:ring-blue-500"
              />
              <div>
                <span className="text-sm font-semibold text-slate-800 dark:text-slate-200 block">
                  IQR Outlier Capping (Conservative 3x IQR)
                </span>
                <span className="text-xs text-slate-500 dark:text-slate-400">
                  Caps extreme monetary and duration values exceeding 3x Interquartile Range.
                </span>
              </div>
            </label>
          </div>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-slate-200 dark:border-slate-800">
          <p className="text-xs text-slate-400">
            Never modifies raw_clickstream.csv. Writes a separate cleaned_clickstream.csv in session directory.
          </p>
          <button
            onClick={handleRunPreprocessing}
            disabled={loading}
            className="flex items-center space-x-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-colors disabled:opacity-50"
          >
            <Play className="w-4 h-4 fill-current" />
            <span>{loading ? 'Executing in R...' : 'Run Preprocessing Pipeline'}</span>
          </button>
        </div>
      </div>

      {loading && <LoadingState message="R data.table is executing transformations..." />}

      {/* Preprocessing Summary Comparison */}
      {result && (
        <div className="bg-white dark:bg-slate-900 p-6 rounded-xl border border-emerald-200 dark:border-emerald-900/60 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
              <h3 className="text-base font-semibold text-slate-800 dark:text-slate-100">
                Preprocessing Completed Successfully
              </h3>
            </div>
            <Link
              to="/eda"
              className="flex items-center space-x-1 text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline"
            >
              <span>Proceed to EDA</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2">
            <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60">
              <span className="text-xs text-slate-400 uppercase font-semibold">Row Count</span>
              <div className="mt-1 flex items-baseline space-x-2">
                <span className="text-xl font-bold text-slate-900 dark:text-slate-100">
                  {result.summary.final_rows.toLocaleString()}
                </span>
                <span className="text-xs text-slate-400">
                  (was {result.summary.initial_rows.toLocaleString()})
                </span>
              </div>
              <span className="text-[11px] text-emerald-600">
                {result.summary.rows_removed} rows filtered
              </span>
            </div>

            <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60">
              <span className="text-xs text-slate-400 uppercase font-semibold">Duplicates Cleaned</span>
              <p className="text-xl font-bold text-slate-900 dark:text-slate-100 mt-1">
                {result.summary.duplicates_removed.toLocaleString()}
              </p>
              <span className="text-[11px] text-slate-400">Exact duplicate events removed</span>
            </div>

            <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60">
              <span className="text-xs text-slate-400 uppercase font-semibold">Imputed Values</span>
              <p className="text-xl font-bold text-slate-900 dark:text-slate-100 mt-1">
                {result.summary.imputed_values.toLocaleString()}
              </p>
              <span className="text-[11px] text-slate-400">Median/Mode filled values</span>
            </div>

            <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60">
              <span className="text-xs text-slate-400 uppercase font-semibold">Outliers Handled</span>
              <p className="text-xl font-bold text-slate-900 dark:text-slate-100 mt-1">
                {result.summary.outliers_handled.toLocaleString()}
              </p>
              <span className="text-[11px] text-slate-400">3x IQR values capped</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
