import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { SegmentationResponse } from '../types';
import { DynamicChart } from '../components/DynamicChart';
import { LoadingState, ErrorState, EmptyState } from '../components/StatusStates';
import { Users2, Download, HelpCircle, Layers, Sparkles } from 'lucide-react';

export const CustomerSegmentation: React.FC<{ isDark: boolean; onLoadDefault: () => void }> = ({
  isDark,
  onLoadDefault,
}) => {
  const [data, setData] = useState<SegmentationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedK, setSelectedK] = useState<number>(4);

  const fetchSegmentation = async (kVal: number = selectedK) => {
    setLoading(true);
    setError(null);
    try {
      const resp = await api.get('/r/segmentation/run', { params: { k: kVal } });
      setData(resp.data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSegmentation(selectedK);
  }, [selectedK]);

  if (loading && !data) return <LoadingState message="Executing RFM scoring and k-means clustering in R (cluster package)..." />;
  if (error) {
    if (error.includes('No dataset uploaded')) {
      return (
        <EmptyState
          title="No Customer Data Loaded"
          description="Upload clickstream data to perform RFM scoring and k-means customer segmentation."
          onAction={onLoadDefault}
        />
      );
    }
    return <ErrorState message={error} onRetry={() => fetchSegmentation(selectedK)} />;
  }
  if (!data) return null;

  // Chart 1: Silhouette Score Evaluation across k = 2 to 6
  const silChartOption = {
    tooltip: { trigger: 'axis', formatter: 'k = {b}: Silhouette Score = <b>{c}</b>' },
    xAxis: {
      type: 'category',
      data: data.silhouette_analysis.map((s) => `k = ${s.k}`),
      name: 'Number of Clusters (k)',
    },
    yAxis: { type: 'value', name: 'Avg Silhouette Width', min: 0 },
    series: [
      {
        name: 'Silhouette Score',
        type: 'bar',
        data: data.silhouette_analysis.map((s) => s.score),
        itemStyle: {
          color: (params: any) =>
            data.silhouette_analysis[params.dataIndex]?.k === selectedK ? '#2563eb' : '#93c5fd',
          borderRadius: [4, 4, 0, 0],
        },
      },
    ],
  };

  // Chart 2: 2D PCA Cluster Scatter Plot
  const clusterColors = ['#2563eb', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4'];
  const scatterSeries = (data.segments_summary || []).map((seg) => {
    const pts = data.scatter_data
      .filter((p) => p.cluster === seg.cluster)
      .map((p) => [p.pc1, p.pc2, p.recency, p.frequency, p.monetary, p.id]);
    return {
      name: seg.segment_name,
      type: 'scatter',
      data: pts,
      symbolSize: 8,
      itemStyle: { color: clusterColors[(seg.cluster - 1) % clusterColors.length] },
    };
  });

  const pcaScatterOption = {
    tooltip: {
      formatter: (p: any) => {
        return `<b>${p.seriesName}</b><br/>Cust: ${p.data[5]}<br/>Recency: ${p.data[2]}d<br/>Freq: ${p.data[3]}<br/>Monetary: $${p.data[4]}`;
      },
    },
    legend: { top: 0, type: 'scroll' },
    xAxis: { type: 'value', name: 'PCA Component 1' },
    yAxis: { type: 'value', name: 'PCA Component 2' },
    series: scatterSeries,
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            Customer RFM Segmentation & K-Means Clustering
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Automated Recency, Frequency, Monetary (RFM) scoring with silhouette-evaluated k-means clustering in R.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 px-3 py-1.5 rounded-lg text-xs">
            <span className="text-slate-700 dark:text-slate-300 font-medium">Clusters (k):</span>
            <select
              value={selectedK}
              onChange={(e) => setSelectedK(Number(e.target.value))}
              className="bg-transparent font-bold text-blue-600 dark:text-blue-400 outline-hidden cursor-pointer"
            >
              {[2, 3, 4, 5, 6].map((k) => (
                <option key={k} value={k} className="bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100">
                  {k} Clusters
                </option>
              ))}
            </select>
          </div>
          <a
            href="http://localhost:8000/api/export/csv?file_type=rfm_segments"
            download="rfm_segments.csv"
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Segments CSV</span>
          </a>
        </div>
      </div>

      {/* Silhouette & PCA Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Silhouette Analysis */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 flex items-center">
              <Sparkles className="w-4 h-4 mr-2 text-blue-600" />
              Silhouette Analysis for Optimal k Selection
            </h3>
            <span className="text-xs text-slate-400 font-mono">cluster::silhouette</span>
          </div>
          <DynamicChart option={silChartOption} height={320} isDark={isDark} />
        </div>

        {/* 2D PCA Cluster Scatter */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              Customer Clusters (PCA Projection)
            </h3>
            <span className="text-xs text-slate-400">Log1p Normalized</span>
          </div>
          <DynamicChart option={pcaScatterOption} height={320} isDark={isDark} />
        </div>
      </div>

      {/* Segments Summary Table */}
      <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
        <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3">
          Identified Customer Cohort Profiles & Spend Breakdown
        </h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-xs font-mono">
            <thead className="bg-slate-50 dark:bg-slate-800/60">
              <tr>
                <th className="px-3 py-2 text-left font-semibold text-slate-700 dark:text-slate-300">Cluster</th>
                <th className="px-3 py-2 text-left font-semibold text-slate-700 dark:text-slate-300">Segment Name</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Customers</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">% Share</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Avg Recency (Days)</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Avg Frequency</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Avg Monetary ($)</th>
                <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Total Revenue ($)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {data.segments_summary.map((seg) => (
                <tr key={seg.cluster} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                  <td className="px-3 py-2 text-slate-400 font-bold">C{seg.cluster}</td>
                  <td className="px-3 py-2 font-bold text-slate-800 dark:text-slate-200">{seg.segment_name}</td>
                  <td className="px-3 py-2 text-right text-slate-600 dark:text-slate-400">{seg.customers.toLocaleString()}</td>
                  <td className="px-3 py-2 text-right text-blue-600 dark:text-blue-400 font-semibold">{seg.pct_customers}%</td>
                  <td className="px-3 py-2 text-right text-slate-600 dark:text-slate-400">{seg.avg_recency_days}d</td>
                  <td className="px-3 py-2 text-right text-slate-600 dark:text-slate-400">{seg.avg_frequency}</td>
                  <td className="px-3 py-2 text-right text-slate-800 dark:text-slate-200 font-bold">${seg.avg_monetary.toLocaleString()}</td>
                  <td className="px-3 py-2 text-right text-emerald-600 dark:text-emerald-400 font-bold">${seg.total_revenue.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Exact Segment Rules */}
      <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
        <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3 flex items-center">
          <HelpCircle className="w-4 h-4 mr-2 text-slate-400" />
          Segment Classification Rules & Business Strategy
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.exact_rules.map((rule, idx) => (
            <div key={idx} className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60">
              <span className="text-xs font-bold text-blue-600 dark:text-blue-400 block">{rule.segment}</span>
              <p className="text-xs text-slate-600 dark:text-slate-300 mt-1">{rule.condition}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
