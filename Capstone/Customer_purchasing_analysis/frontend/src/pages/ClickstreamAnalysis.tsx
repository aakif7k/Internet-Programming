import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { ClickstreamResponse } from '../types';
import { DynamicChart } from '../components/DynamicChart';
import { MetricCard } from '../components/MetricCard';
import { LoadingState, ErrorState, EmptyState } from '../components/StatusStates';
import {
  MousePointerClick,
  Footprints,
  Compass,
  ArrowRight,
  TrendingDown,
  Clock
} from 'lucide-react';

export const ClickstreamAnalysis: React.FC<{ isDark: boolean; onLoadDefault: () => void }> = ({
  isDark,
  onLoadDefault,
}) => {
  const [data, setData] = useState<ClickstreamResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await api.get('/r/clickstream/analysis');
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

  if (loading) return <LoadingState message="Analyzing clickstream sequences and transitions in R..." />;
  if (error) {
    if (error.includes('No dataset uploaded')) {
      return (
        <EmptyState
          title="No Clickstream Data Loaded"
          description="Upload your clickstream dataset to analyze navigation paths and page transitions."
          onAction={onLoadDefault}
        />
      );
    }
    return <ErrorState message={error} onRetry={fetchData} />;
  }
  if (!data) return null;

  // Chart 1: Most Visited Pages
  const pagesChartOption = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: { type: 'value', name: 'Pageviews' },
    yAxis: {
      type: 'category',
      data: (data.pages || []).slice(0, 10).map((p) => p.page_url).reverse(),
      axisLabel: { width: 120, overflow: 'truncate' },
    },
    series: [
      {
        name: 'Views',
        type: 'bar',
        data: (data.pages || []).slice(0, 10).map((p) => p.views).reverse(),
        itemStyle: { color: '#0c87eb', borderRadius: [0, 4, 4, 0] },
      },
    ],
  };

  // Chart 2: Event Transitions Sankey / Heatmap Matrix
  const uniqueEvents = data.transitions?.events || [];
  const linkMatrixData: [number, number, number][] = [];
  if (data.transitions?.links) {
    data.transitions.links.forEach((l) => {
      const sIdx = uniqueEvents.indexOf(l.source);
      const tIdx = uniqueEvents.indexOf(l.target);
      if (sIdx >= 0 && tIdx >= 0) {
        linkMatrixData.push([sIdx, tIdx, l.probability]);
      }
    });
  }

  const transitionHeatmapOption = {
    tooltip: {
      position: 'top',
      formatter: (p: any) => {
        const from = uniqueEvents[p.data[0]];
        const to = uniqueEvents[p.data[1]];
        return `<b>${from}</b> &rarr; <b>${to}</b><br/>Transition Prob: <b>${p.data[2]}</b>`;
      },
    },
    grid: { height: '65%', top: '10%' },
    xAxis: {
      type: 'category',
      data: uniqueEvents,
      axisLabel: { rotate: 30, interval: 0, fontSize: 10 },
      name: 'From Event',
      nameLocation: 'middle',
      nameGap: 30,
    },
    yAxis: {
      type: 'category',
      data: uniqueEvents,
      axisLabel: { fontSize: 10 },
      name: 'To Event',
    },
    visualMap: {
      min: 0,
      max: 1,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: ['#f8fafc', '#93c5fd', '#1d4ed8'],
      },
    },
    series: [
      {
        name: 'Transition Probability',
        type: 'heatmap',
        data: linkMatrixData,
        label: { show: true, fontSize: 9 },
      },
    ],
  };

  return (
    <div className="space-y-6">
      <div className="pb-4 border-b border-slate-200 dark:border-slate-800">
        <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
          Clickstream Navigation & Transition Analysis
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Sequential path mining, Markov transition probabilities, bounce metrics, and page engagement.
        </p>
      </div>

      {/* Engagement KPI cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard
          title="Bounce Rate"
          value={`${data.engagement.bounce_rate}%`}
          subtitle={`${data.engagement.bounce_count} single-event visits`}
          icon={TrendingDown}
          badge="Bounces"
          badgeColor="amber"
        />
        <MetricCard
          title="Avg Events Per Session"
          value={data.engagement.avg_events_per_session}
          subtitle="Interaction depth"
          icon={Compass}
          badge="Depth"
          badgeColor="blue"
        />
        <MetricCard
          title="Total Distinct Paths"
          value={data.top_paths.length}
          subtitle="Top navigation patterns identified"
          icon={Footprints}
          badge="Sequences"
          badgeColor="purple"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Most Visited Pages */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3">
            Top Visited Page URLs
          </h3>
          <DynamicChart option={pagesChartOption} height={350} isDark={isDark} />
        </div>

        {/* Transition Probabilities Heatmap */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              Markov Event Transition Matrix (P(Next | Prev))
            </h3>
            <span className="text-xs text-slate-400">R sequential pairs</span>
          </div>
          <DynamicChart option={transitionHeatmapOption} height={350} isDark={isDark} />
        </div>
      </div>

      {/* Top Navigation Paths Table */}
      <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
        <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-3 flex items-center">
          <Footprints className="w-4 h-4 mr-2 text-blue-600" />
          Top Sequential Navigation Paths (First 4 Touchpoints)
        </h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-xs">
            <thead className="bg-slate-50 dark:bg-slate-800/60">
              <tr>
                <th className="px-4 py-2.5 text-left font-semibold text-slate-600 dark:text-slate-300">Rank</th>
                <th className="px-4 py-2.5 text-left font-semibold text-slate-600 dark:text-slate-300">Navigation Journey</th>
                <th className="px-4 py-2.5 text-right font-semibold text-slate-600 dark:text-slate-300">Sessions</th>
                <th className="px-4 py-2.5 text-right font-semibold text-slate-600 dark:text-slate-300">% of Cohort</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-mono">
              {data.top_paths.map((p, idx) => (
                <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                  <td className="px-4 py-2 text-slate-400 font-bold">#{idx + 1}</td>
                  <td className="px-4 py-2 text-slate-800 dark:text-slate-200 font-medium">
                    <span className="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300">
                      {p.path}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-right text-slate-600 dark:text-slate-400">{p.count.toLocaleString()}</td>
                  <td className="px-4 py-2 text-right text-blue-600 dark:text-blue-400 font-semibold">{p.pct}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
