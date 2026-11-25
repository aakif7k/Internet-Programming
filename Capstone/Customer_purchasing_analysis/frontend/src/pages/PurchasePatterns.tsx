import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { PurchasePatternsResponse } from '../types';
import { DynamicChart } from '../components/DynamicChart';
import { LoadingState, ErrorState, EmptyState } from '../components/StatusStates';
import { ShoppingBag, DollarSign, Calendar, Clock, BarChart } from 'lucide-react';

export const PurchasePatterns: React.FC<{ isDark: boolean; onLoadDefault: () => void }> = ({
  isDark,
  onLoadDefault,
}) => {
  const [data, setData] = useState<PurchasePatternsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await api.get('/r/purchase/patterns');
      setData(resp.data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <LoadingState message="Analyzing purchase patterns and product views in R..." />;
  if (error) {
    if (error.includes('No dataset uploaded')) {
      return (
        <EmptyState
          title="No Purchase Data Loaded"
          description="Upload your clickstream data to analyze category conversion rates and order values."
          onAction={onLoadDefault}
        />
      );
    }
    return <ErrorState message={error} onRetry={fetchData} />;
  }
  if (!data) return null;

  // Chart 1: Viewed vs Purchased Categories
  const catChartOption = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { top: 0 },
    xAxis: {
      type: 'category',
      data: (data.categories || []).map((c) => c.category),
      axisLabel: { rotate: 25 },
    },
    yAxis: [
      { type: 'value', name: 'Views / Purchases' },
      { type: 'value', name: 'Conv Ratio (%)', position: 'right' },
    ],
    series: [
      {
        name: 'Views',
        type: 'bar',
        data: (data.categories || []).map((c) => c.views),
        itemStyle: { color: '#93c5fd', borderRadius: [4, 4, 0, 0] },
      },
      {
        name: 'Purchases',
        type: 'bar',
        data: (data.categories || []).map((c) => c.purchases),
        itemStyle: { color: '#3b82f6', borderRadius: [4, 4, 0, 0] },
      },
      {
        name: 'Conversion Ratio (%)',
        type: 'line',
        yAxisIndex: 1,
        data: (data.categories || []).map((c) => c.conversion_ratio),
        itemStyle: { color: '#10b981' },
      },
    ],
  };

  // Chart 2: Hourly Purchase Patterns
  const hourlyChartOption = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: (data.hourly || []).map((h) => `${h.hour}:00`),
    },
    yAxis: [
      { type: 'value', name: 'Orders' },
      { type: 'value', name: 'Revenue ($)', position: 'right' },
    ],
    series: [
      {
        name: 'Orders',
        type: 'bar',
        data: (data.hourly || []).map((h) => h.orders),
        itemStyle: { color: '#818cf8', borderRadius: [4, 4, 0, 0] },
      },
      {
        name: 'Revenue ($)',
        type: 'line',
        smooth: true,
        yAxisIndex: 1,
        data: (data.hourly || []).map((h) => h.revenue),
        itemStyle: { color: '#10b981' },
      },
    ],
  };

  // Chart 3: Day of Week Patterns
  const dowChartOption = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: {
      type: 'category',
      data: (data.day_of_week || []).map((d) => d.day),
    },
    yAxis: { type: 'value', name: 'Orders' },
    series: [
      {
        name: 'Orders',
        type: 'bar',
        data: (data.day_of_week || []).map((d) => d.orders),
        itemStyle: { color: '#f59e0b', borderRadius: [4, 4, 0, 0] },
      },
    ],
  };

  return (
    <div className="space-y-6">
      <div className="pb-4 border-b border-slate-200 dark:border-slate-800">
        <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
          Customer Purchase Patterns & AOV Analysis
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Examine category-level view-to-purchase ratios, average order value segmentation, and temporal buying patterns.
        </p>
      </div>

      {/* Viewed vs Purchased Categories */}
      <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
        <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3">
          Top Product Categories: Views vs Purchases & Conversion Ratio
        </h3>
        <DynamicChart option={catChartOption} height={340} isDark={isDark} />
      </div>

      {/* Hourly and Day-of-Week Patterns */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3 flex items-center">
            <Clock className="w-4 h-4 mr-2 text-indigo-600" />
            Purchases & Revenue by Hour of Day
          </h3>
          <DynamicChart option={hourlyChartOption} height={300} isDark={isDark} />
        </div>

        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3 flex items-center">
            <Calendar className="w-4 h-4 mr-2 text-amber-500" />
            Order Volume by Day of Week
          </h3>
          <DynamicChart option={dowChartOption} height={300} isDark={isDark} />
        </div>
      </div>

      {/* AOV Breakdown Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AOV by Device */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3">
            Average Order Value (AOV) by Device Type
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-xs font-mono">
              <thead className="bg-slate-50 dark:bg-slate-800/60">
                <tr>
                  <th className="px-3 py-2 text-left font-semibold text-slate-700 dark:text-slate-300">Device</th>
                  <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Orders</th>
                  <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Revenue</th>
                  <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">AOV ($)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {data.aov_by_device.map((d) => (
                  <tr key={d.dimension} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td className="px-3 py-1.5 font-medium text-slate-800 dark:text-slate-200">{d.dimension}</td>
                    <td className="px-3 py-1.5 text-right text-slate-500">{d.orders.toLocaleString()}</td>
                    <td className="px-3 py-1.5 text-right text-slate-500">${d.revenue.toLocaleString()}</td>
                    <td className="px-3 py-1.5 text-right text-emerald-600 dark:text-emerald-400 font-bold">${d.aov}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* AOV by Traffic Source */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3">
            Average Order Value (AOV) by Traffic Source
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-xs font-mono">
              <thead className="bg-slate-50 dark:bg-slate-800/60">
                <tr>
                  <th className="px-3 py-2 text-left font-semibold text-slate-700 dark:text-slate-300">Traffic Source</th>
                  <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Orders</th>
                  <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">Revenue</th>
                  <th className="px-3 py-2 text-right font-semibold text-slate-700 dark:text-slate-300">AOV ($)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {data.aov_by_traffic.map((t) => (
                  <tr key={t.dimension} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td className="px-3 py-1.5 font-medium text-slate-800 dark:text-slate-200">{t.dimension}</td>
                    <td className="px-3 py-1.5 text-right text-slate-500">{t.orders.toLocaleString()}</td>
                    <td className="px-3 py-1.5 text-right text-slate-500">${t.revenue.toLocaleString()}</td>
                    <td className="px-3 py-1.5 text-right text-emerald-600 dark:text-emerald-400 font-bold">${t.aov}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
