import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { OverviewKPIs } from '../types';
import { MetricCard } from '../components/MetricCard';
import { DynamicChart } from '../components/DynamicChart';
import { LoadingState, ErrorState, EmptyState } from '../components/StatusStates';
import {
  Activity,
  Users,
  Compass,
  TrendingUp,
  DollarSign,
  ShoppingCart,
  ArrowRight,
  Database,
  Sliders,
  Brain
} from 'lucide-react';
import { Link } from 'react-router-dom';

export const Overview: React.FC<{ isDark: boolean; onLoadDefault: () => void }> = ({ isDark, onLoadDefault }) => {
  const [data, setData] = useState<OverviewKPIs | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await api.get('/r/overview/kpis');
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

  if (loading) return <LoadingState message="Loading dataset overview KPIs from R..." />;
  if (error) {
    if (error.includes('No dataset uploaded')) {
      return (
        <EmptyState
          title="No Clickstream Data Loaded"
          description="Upload your clickstream dataset or load the pre-configured 10,000 session capstone dataset to begin the analysis."
          onAction={onLoadDefault}
          actionText="Load Capstone Dataset"
        />
      );
    }
    return <ErrorState message={error} onRetry={fetchData} />;
  }
  if (!data) return null;

  // Chart 1: Event Breakdown
  const eventChartOption = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: {
      type: 'category',
      data: data.event_breakdown.map((e) => e.name),
      axisLabel: { rotate: 25 },
    },
    yAxis: { type: 'value', name: 'Events' },
    series: [
      {
        name: 'Events',
        type: 'bar',
        data: data.event_breakdown.map((e) => e.count),
        itemStyle: { color: '#0c87eb', borderRadius: [4, 4, 0, 0] },
      },
    ],
  };

  // Chart 2: Device Breakdown Pie
  const deviceChartOption = {
    tooltip: { trigger: 'item', formatter: '{b}: {c} events ({d}%)' },
    legend: { bottom: '0', left: 'center' },
    series: [
      {
        name: 'Device Type',
        type: 'pie',
        radius: ['45%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 8, borderColor: isDark ? '#0f172a' : '#fff', borderWidth: 2 },
        data: data.device_breakdown.map((d) => ({ name: d.name, value: d.events })),
      },
    ],
  };

  // Chart 3: Daily Activity Trend
  const dailyChartOption = {
    tooltip: { trigger: 'axis' },
    legend: { top: 0, right: 10 },
    xAxis: {
      type: 'category',
      data: data.daily_trend.map((d) => d.date),
      boundaryGap: false,
    },
    yAxis: [
      { type: 'value', name: 'Sessions' },
      { type: 'value', name: 'Revenue ($)', position: 'right' },
    ],
    series: [
      {
        name: 'Sessions',
        type: 'line',
        smooth: true,
        data: data.daily_trend.map((d) => d.sessions),
        itemStyle: { color: '#3b82f6' },
        areaStyle: { opacity: 0.15, color: '#3b82f6' },
      },
      {
        name: 'Revenue ($)',
        type: 'line',
        smooth: true,
        yAxisIndex: 1,
        data: data.daily_trend.map((d) => d.revenue),
        itemStyle: { color: '#10b981' },
      },
    ],
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            Clickstream & Conversion Executive Overview
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Real-time R aggregated session metrics, conversion funnel KPIs, and revenue analytics.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Link
            to="/eda"
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-colors"
          >
            <span>Run EDA</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
          <Link
            to="/conversion-prediction"
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-xs transition-colors"
          >
            <Brain className="w-3.5 h-3.5" />
            <span>Train ML Models</span>
          </Link>
        </div>
      </div>

      {/* 6 KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <MetricCard
          title="Total Events"
          value={data.total_events.toLocaleString()}
          subtitle="Clickstream interactions"
          icon={Activity}
          badge="Raw Events"
          badgeColor="blue"
        />
        <MetricCard
          title="Total Sessions"
          value={data.total_sessions.toLocaleString()}
          subtitle="Identified user visits"
          icon={Compass}
          badge="Sessions"
          badgeColor="purple"
        />
        <MetricCard
          title="Customers"
          value={data.total_customers.toLocaleString()}
          subtitle="Unique client profiles"
          icon={Users}
          badge="Profiles"
          badgeColor="blue"
        />
        <MetricCard
          title="Conversion Rate"
          value={`${data.conversion_rate}%`}
          subtitle={`${data.converted_sessions.toLocaleString()} converted`}
          icon={TrendingUp}
          badge="Funnel"
          badgeColor="green"
        />
        <MetricCard
          title="Total Revenue"
          value={`$${data.total_revenue.toLocaleString()}`}
          subtitle="Sum of purchase orders"
          icon={DollarSign}
          badge="Purchases"
          badgeColor="green"
        />
        <MetricCard
          title="Avg Order Value"
          value={`$${data.avg_order_value.toLocaleString()}`}
          subtitle="Revenue per conversion"
          icon={ShoppingCart}
          badge="AOV"
          badgeColor="amber"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              Daily Activity: Sessions vs Revenue Trend
            </h3>
            <span className="text-xs text-slate-400">R time aggregation</span>
          </div>
          <DynamicChart option={dailyChartOption} height={320} isDark={isDark} />
        </div>

        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              Device Distribution
            </h3>
            <span className="text-xs text-slate-400">By events</span>
          </div>
          <DynamicChart option={deviceChartOption} height={320} isDark={isDark} />
        </div>
      </div>

      {/* Event Breakdown */}
      <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              Clickstream Event Distribution
            </h3>
            <p className="text-xs text-slate-400">Volume across journey touchpoints</p>
          </div>
        </div>
        <DynamicChart option={eventChartOption} height={280} isDark={isDark} />
      </div>
    </div>
  );
};
