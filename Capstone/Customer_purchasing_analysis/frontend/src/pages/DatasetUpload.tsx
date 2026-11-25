import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { DatasetInspectResponse } from '../types';
import { LoadingState, ErrorState } from '../components/StatusStates';
import {
  UploadCloud,
  FileSpreadsheet,
  CheckCircle2,
  Trash2,
  Sparkles,
  ArrowRightLeft,
  AlertTriangle,
  Info
} from 'lucide-react';

export const DatasetUpload: React.FC<{
  onDatasetChanged: () => void;
  onLoadDefault: () => void;
  loadingAction: boolean;
}> = ({ onDatasetChanged, onLoadDefault, loadingAction }) => {
  const [data, setData] = useState<DatasetInspectResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [mapping, setMapping] = useState<Record<string, string>>({});
  const [savingMapping, setSavingMapping] = useState(false);
  const [mapSuccess, setMapSuccess] = useState(false);

  const fetchInspection = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await api.post('/r/dataset/inspect', {});
      if (resp.data.status === 'empty') {
        setData(null);
        return;
      }
      if (resp.data.status === 'error') {
        setError(resp.data.error || resp.data.message || 'Dataset inspection error in R');
        setData(null);
        return;
      }
      setData(resp.data);
      if (resp.data.columns) {
        // Initialize mapping with saved or auto-detected
        const initial = { ...resp.data.auto_mapping, ...resp.data.saved_mapping };
        setMapping(initial);
      }
    } catch (err: any) {
      if (err.response?.status === 400 && err.response?.data?.message?.includes('No dataset')) {
        setData(null);
      } else {
        setError(err.response?.data?.error || err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInspection();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setError(null);
    try {
      await api.post('/dataset/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      await fetchInspection();
      onDatasetChanged();
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleSaveMapping = async () => {
    setSavingMapping(true);
    setMapSuccess(false);
    try {
      await api.post('/dataset/field-mapping', { mapping });
      setMapSuccess(true);
      setTimeout(() => setMapSuccess(false), 3000);
      onDatasetChanged();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSavingMapping(false);
    }
  };

  const handleClear = async () => {
    if (!confirm('Are you sure you want to clear the dataset for this session?')) return;
    try {
      await api.delete('/dataset/clear');
      setData(null);
      onDatasetChanged();
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            Dataset Upload & Field Mapping
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Upload custom website clickstream CSV or inspect and map columns for statistical analysis.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={onLoadDefault}
            disabled={loadingAction || uploading}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-xs transition-colors disabled:opacity-50"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Load Capstone Dataset (10k Sessions)</span>
          </button>
          {data?.status === 'ready' && (
            <button
              onClick={handleClear}
              className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/50 border border-rose-200 dark:border-rose-900 transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear</span>
            </button>
          )}
        </div>
      </div>

      {error && <ErrorState message={error} onRetry={fetchInspection} />}

      {/* Upload Dropzone */}
      <div className="bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
        <label
          htmlFor="csv-upload"
          className="border-2 border-dashed border-slate-300 dark:border-slate-700 hover:border-blue-500 dark:hover:border-blue-500 rounded-xl p-8 flex flex-col items-center justify-center cursor-pointer transition-colors bg-slate-50/50 dark:bg-slate-800/20"
        >
          <UploadCloud className="w-10 h-10 text-blue-500 mb-3 animate-bounce" />
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">
            Click to upload or drag and drop clickstream CSV
          </p>
          <p className="text-xs text-slate-400 mt-1">
            CSV files up to 100MB supported. Stream-validated and stored in isolated session folder.
          </p>
          <input
            id="csv-upload"
            type="file"
            accept=".csv"
            onChange={handleFileUpload}
            disabled={uploading}
            className="hidden"
          />
        </label>
        {uploading && <LoadingState message="Uploading and streaming CSV to session storage..." />}
      </div>

      {loading && !uploading && <LoadingState message="Analyzing dataset structure in R..." />}

      {data?.status === 'ready' && data.columns && (
        <>
          {/* Metadata Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <span className="text-xs text-slate-400 uppercase font-semibold">Active File</span>
              <p className="text-base font-bold text-slate-800 dark:text-slate-100 truncate mt-1">
                {data.filename}
              </p>
              <span className="text-[11px] text-blue-600 dark:text-blue-400 capitalize">
                {data.active_type} dataset
              </span>
            </div>
            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <span className="text-xs text-slate-400 uppercase font-semibold">Total Rows</span>
              <p className="text-2xl font-bold text-slate-800 dark:text-slate-100 mt-1">
                {data.total_rows.toLocaleString()}
              </p>
              <span className="text-[11px] text-slate-400">Total event logs</span>
            </div>
            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <span className="text-xs text-slate-400 uppercase font-semibold">Total Columns</span>
              <p className="text-2xl font-bold text-slate-800 dark:text-slate-100 mt-1">
                {data.total_columns}
              </p>
              <span className="text-[11px] text-slate-400">Detected schema fields</span>
            </div>
            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <span className="text-xs text-slate-400 uppercase font-semibold">Est. Duplicates</span>
              <p className="text-2xl font-bold text-slate-800 dark:text-slate-100 mt-1">
                {data.duplicate_count_est}
              </p>
              <span className="text-[11px] text-amber-500">In 25k row sample</span>
            </div>
          </div>

          {/* Field Mapping Section */}
          <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-2">
              <div className="flex items-center space-x-2">
                <ArrowRightLeft className="w-5 h-5 text-blue-600" />
                <h3 className="text-base font-semibold text-slate-800 dark:text-slate-100">
                  Field Mapping (Auto-detected)
                </h3>
              </div>
              <div className="flex items-center space-x-2">
                {mapSuccess && (
                  <span className="text-xs text-emerald-600 font-medium flex items-center">
                    <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Mapping saved!
                  </span>
                )}
                <button
                  onClick={handleSaveMapping}
                  disabled={savingMapping}
                  className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold shadow-xs disabled:opacity-50"
                >
                  {savingMapping ? 'Saving...' : 'Save Field Mapping'}
                </button>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 pt-4 text-xs">
              {Object.keys(data.auto_mapping || {}).slice(0, 18).map((stdField) => (
                <div
                  key={stdField}
                  className="flex items-center justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700"
                >
                  <span className="font-mono text-slate-600 dark:text-slate-300 font-medium truncate mr-2">
                    {stdField}
                  </span>
                  <select
                    value={mapping[stdField] || ''}
                    onChange={(e) => setMapping({ ...mapping, [stdField]: e.target.value })}
                    className="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded px-2 py-1 text-slate-800 dark:text-slate-200 text-xs max-w-[140px]"
                  >
                    <option value="">-- None --</option>
                    {data.columns.map((col) => (
                      <option key={col.name} value={col.name}>
                        {col.name}
                      </option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          </div>

          {/* Schema & Missing Values Table */}
          <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
            <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3">
              Column Data Types & Missing Value Audit ({data.columns.length} columns)
            </h3>
            <div className="overflow-x-auto max-h-80 overflow-y-auto">
              <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-xs">
                <thead className="bg-slate-50 dark:bg-slate-800/60 sticky top-0">
                  <tr>
                    <th className="px-3 py-2 text-left font-semibold text-slate-600 dark:text-slate-300">Column Name</th>
                    <th className="px-3 py-2 text-left font-semibold text-slate-600 dark:text-slate-300">Data Type</th>
                    <th className="px-3 py-2 text-left font-semibold text-slate-600 dark:text-slate-300">Missing Count</th>
                    <th className="px-3 py-2 text-left font-semibold text-slate-600 dark:text-slate-300">Missing %</th>
                    <th className="px-3 py-2 text-left font-semibold text-slate-600 dark:text-slate-300">Sample Values</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-mono">
                  {data.columns.map((col) => (
                    <tr key={col.name} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                      <td className="px-3 py-2 font-medium text-slate-800 dark:text-slate-200">{col.name}</td>
                      <td className="px-3 py-2">
                        <span className="px-1.5 py-0.5 rounded text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                          {col.type}
                        </span>
                      </td>
                      <td className="px-3 py-2 text-slate-600 dark:text-slate-400">{col.missing_count}</td>
                      <td className="px-3 py-2">
                        <span className={`px-1.5 py-0.5 rounded text-[10px] ${
                          col.missing_pct > 20
                            ? 'bg-rose-50 text-rose-600 dark:bg-rose-950/60 dark:text-rose-400'
                            : col.missing_pct > 0
                            ? 'bg-amber-50 text-amber-600 dark:bg-amber-950/60 dark:text-amber-400'
                            : 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400'
                        }`}>
                          {col.missing_pct}%
                        </span>
                      </td>
                      <td className="px-3 py-2 text-slate-500 truncate max-w-xs">
                        {col.sample_values ? col.sample_values.join(', ') : '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* First 50 Rows Preview */}
          <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                Dataset Preview (First 50 Rows, All {data.columns.length} Columns)
              </h3>
              <span className="text-xs text-slate-400">Scroll horizontally to view all fields</span>
            </div>
            <div className="overflow-x-auto max-h-96 overflow-y-auto border border-slate-200 dark:border-slate-800 rounded-lg">
              <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-xs font-mono">
                <thead className="bg-slate-100 dark:bg-slate-800 sticky top-0">
                  <tr>
                    {data.columns.map((c) => (
                      <th key={c.name} className="px-3 py-2 text-left font-semibold text-slate-700 dark:text-slate-300 whitespace-nowrap">
                        {c.name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {data.preview.map((row, idx) => (
                    <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                      {data.columns.map((c) => (
                        <td key={c.name} className="px-3 py-1.5 text-slate-600 dark:text-slate-400 whitespace-nowrap">
                          {row[c.name] !== undefined && row[c.name] !== null ? String(row[c.name]) : '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
