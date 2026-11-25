import React from 'react';
import { Sun, Moon, Database, Upload, RefreshCw, Trash2 } from 'lucide-react';
import { DatasetStatus } from '../types';

interface HeaderProps {
  collapsed: boolean;
  isDark: boolean;
  toggleDarkMode: () => void;
  datasetStatus: DatasetStatus | null;
  onLoadDefault: () => void;
  onClearDataset: () => void;
  loadingAction: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  collapsed,
  isDark,
  toggleDarkMode,
  datasetStatus,
  onLoadDefault,
  onClearDataset,
  loadingAction,
}) => {
  const hasData = datasetStatus?.raw_uploaded || datasetStatus?.cleaned_available;

  return (
    <header
      className={`fixed top-0 right-0 z-30 h-16 bg-white/95 dark:bg-slate-900/95 backdrop-blur border-b border-slate-200 dark:border-slate-800 transition-all duration-300 ease-in-out px-6 flex items-center justify-between ${
        collapsed ? 'left-20' : 'left-64'
      }`}
    >
      <div className="flex items-center space-x-3">
        <h1 className="text-base font-semibold text-slate-800 dark:text-slate-100 truncate max-w-xl">
          Customer Clickstream & Revenue ML Studio
        </h1>
        {hasData && (
          <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 dark:bg-emerald-950/70 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5 animate-pulse" />
            {datasetStatus?.cleaned_available ? 'Cleaned Dataset Ready' : 'Raw Dataset Loaded'}
          </span>
        )}
      </div>

      <div className="flex items-center space-x-2">
        {/* Quick Load Default Dataset Button */}
        {!hasData && (
          <button
            onClick={onLoadDefault}
            disabled={loadingAction}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-sm transition-colors disabled:opacity-50"
            title="Load default 10k sessions dataset instantly"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Load Capstone Dataset</span>
          </button>
        )}

        {hasData && (
          <button
            onClick={onClearDataset}
            disabled={loadingAction}
            className="flex items-center space-x-1 px-2.5 py-1.5 text-xs font-medium rounded-lg text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/50 border border-transparent hover:border-rose-200 dark:hover:border-rose-900 transition-colors"
            title="Clear current session data"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span className="hidden md:inline">Clear Data</span>
          </button>
        )}

        {/* Dark Mode Toggle */}
        <button
          onClick={toggleDarkMode}
          className="p-2 rounded-lg text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
        </button>
      </div>
    </header>
  );
};
