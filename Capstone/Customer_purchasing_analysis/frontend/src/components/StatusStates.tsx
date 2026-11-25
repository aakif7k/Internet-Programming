import React from 'react';
import { Loader2, AlertCircle, Database, Upload } from 'lucide-react';

export const LoadingState: React.FC<{ message?: string }> = ({ message = 'Processing in R Analytics engine...' }) => (
  <div className="flex flex-col items-center justify-center p-12 text-center">
    <Loader2 className="w-8 h-8 text-blue-600 animate-spin mb-3" />
    <p className="text-sm font-medium text-slate-600 dark:text-slate-300">{message}</p>
    <p className="text-xs text-slate-400 dark:text-slate-500 mt-1">R plumber is executing statistical calculations</p>
  </div>
);

export const ErrorState: React.FC<{ message: string; onRetry?: () => void }> = ({ message, onRetry }) => (
  <div className="p-6 rounded-xl border border-rose-200 dark:border-rose-900/60 bg-rose-50/50 dark:bg-rose-950/30 text-rose-900 dark:text-rose-200 my-4">
    <div className="flex items-start space-x-3">
      <AlertCircle className="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0 mt-0.5" />
      <div className="flex-1">
        <h3 className="text-sm font-semibold">Error Executing R Analysis</h3>
        <p className="text-xs text-rose-700 dark:text-rose-300 mt-1 font-mono break-all">{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="mt-3 px-3 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded text-xs font-medium transition-colors"
          >
            Retry Request
          </button>
        )}
      </div>
    </div>
  </div>
);

export const EmptyState: React.FC<{
  title?: string;
  description?: string;
  onAction?: () => void;
  actionText?: string;
}> = ({
  title = 'No Dataset Loaded',
  description = 'Please upload a clickstream CSV or load the sample capstone dataset to view this analysis.',
  onAction,
  actionText = 'Load Capstone Dataset',
}) => (
  <div className="flex flex-col items-center justify-center p-12 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl bg-white/40 dark:bg-slate-900/40">
    <div className="p-3 bg-blue-50 dark:bg-blue-950/60 rounded-full text-blue-600 dark:text-blue-400 mb-3">
      <Database className="w-8 h-8" />
    </div>
    <h3 className="text-base font-semibold text-slate-800 dark:text-slate-100">{title}</h3>
    <p className="text-sm text-slate-500 dark:text-slate-400 max-w-md mt-1 mb-5">{description}</p>
    {onAction && (
      <button
        onClick={onAction}
        className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors"
      >
        <Upload className="w-4 h-4" />
        <span>{actionText}</span>
      </button>
    )}
  </div>
);
