import React, { useEffect, useState } from 'react';
import { api } from '../api/client';
import { FunnelResponse, FunnelStage, DatasetStatus } from '../types';
import { DynamicChart } from '../components/DynamicChart';
import { MetricCard } from '../components/MetricCard';
import { LoadingState, ErrorState, EmptyState } from '../components/StatusStates';
import { Filter, ArrowDown, RefreshCw, CheckCircle2, Sparkles, TrendingDown, Users, ShoppingBag } from 'lucide-react';

export const ConversionFunnel: React.FC<{
  isDark: boolean;
  onLoadDefault: () => void;
  datasetStatus?: DatasetStatus | null;
}> = ({ isDark, onLoadDefault, datasetStatus }) => {
  const [data, setData] = useState<FunnelResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [customStages, setCustomStages] = useState<any[] | null>(null);

  const hasDataset = Boolean(datasetStatus?.active_file);

  const fetchFunnel = async (stagesPayload?: any[]) => {
    if (!hasDataset) return;
    setLoading(true);
    setError(null);
    try {
      const resp = await api.post('/r/funnel/analysis', {
        stages: stagesPayload || customStages,
      });
      if (resp.data.status === 'error') {
        setError(resp.data.message || 'Error computing funnel stages in R.');
      } else {
        setData(resp.data);
        if (!customStages && resp.data.stages) {
          setCustomStages(resp.data.stages);
        }
      }
    } catch (err: any) {
      setError(err.message || 'Error communicating with R funnel endpoint.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (hasDataset) {
      fetchFunnel();
    }
  }, [hasDataset, datasetStatus?.active_file]);

  if (!hasDataset) {
    return (
      <EmptyState
        title="No Clickstream Data Loaded"
        description="Upload your clickstream CSV or click 'Load Capstone Dataset' to compute multi-stage funnel drop-offs and stage-by-stage conversions."
        actionText="Load Capstone Dataset (10k Sessions)"
        onAction={onLoadDefault}
      />
    );
  }

  if (loading && !data) return <LoadingState message="Calculating funnel stage conversions in R..." />;

  if (error) {
    return (
      <div className="space-y-4">
        <ErrorState message={error} onRetry={() => fetchFunnel()} />
        <div className="flex justify-center">
          <button
            onClick={onLoadDefault}
            className="flex items-center space-x-1.5 px-4 py-2 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-xs transition-colors"
          >
            <Sparkles className="w-4 h-4" />
            <span>Reload Capstone Dataset</span>
          </button>
        </div>
      </div>
    );
  }

  if (!data || !data.stages || data.stages.length === 0) {
    return (
      <EmptyState
        title="Funnel Data Unavailable"
        description="Click below to reload the capstone dataset."
        actionText="Load Capstone Dataset (10k Sessions)"
        onAction={onLoadDefault}
      />
    );
  }

  // Derive metrics
  const finalConversions = data.stages[data.stages.length - 1]?.sessions || 0;
  const stagesWithDropoff = [...data.stages].slice(1).sort((a, b) => b.drop_off_rate - a.drop_off_rate);
  const biggestDropoffStage = stagesWithDropoff[0] || null;

  // Funnel ECharts Option
  const funnelChartOption = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} sessions ({d}%)',
    },
    series: [
      {
        name: 'Funnel Stage',
        type: 'funnel',
        left: '10%',
        top: 30,
        bottom: 30,
        width: '80%',
        min: 0,
        max: data.total_entry_sessions,
        minSize: '0%',
        maxSize: '100%',
        sort: 'descending',
        gap: 3,
        label: {
          show: true,
          position: 'inside',
          formatter: '{b}: {c} sessions',
          color: '#fff',
          fontWeight: 'bold',
        },
        data: data.stages.map((st) => ({
          name: st.name,
          value: st.sessions,
        })),
      },
    ],
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            Multi-Stage Conversion Funnel Analysis
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Track user drop-off across custom journey checkpoints: Browse &rarr; Add to Cart &rarr; Checkout &rarr; Purchase.
          </p>
        </div>
        <button
          onClick={() => fetchFunnel()}
          disabled={loading}
          className="flex items-center space-x-1 px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-colors self-start sm:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Recalculate Funnel</span>
        </button>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          title="Total Entry Sessions"
          value={data.total_entry_sessions.toLocaleString()}
          subtitle="Top of funnel journeys"
          icon={Users}
        />
        <MetricCard
          title="Completed Purchases"
          value={finalConversions.toLocaleString()}
          subtitle="Reached final purchase event"
          icon={ShoppingBag}
        />
        <MetricCard
          title="Overall Funnel Conversion"
          value={`${data.overall_funnel_rate}%`}
          subtitle="Entry to purchase success rate"
          icon={CheckCircle2}
        />
        <MetricCard
          title="Biggest Drop-off Stage"
          value={biggestDropoffStage ? biggestDropoffStage.name : 'None'}
          subtitle={biggestDropoffStage ? `${biggestDropoffStage.drop_off_rate}% dropped before next stage` : 'Consistent retention'}
          icon={TrendingDown}
        />
      </div>

      {/* Funnel Chart and Stage Details */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-4">
            ECharts Conversion Funnel Visualization
          </h3>
          <DynamicChart option={funnelChartOption} height={360} isDark={isDark} />
        </div>

        {/* Step-by-Step Breakdown Cards */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs flex flex-col justify-between">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-4">
            Stage-by-Stage Progression & Drop-Off
          </h3>
          <div className="space-y-4">
            {data.stages.map((st, idx) => (
              <div key={st.name} className="relative">
                <div className="flex items-center justify-between p-3.5 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
                  <div className="flex items-center space-x-3">
                    <span className="w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 text-xs font-bold flex items-center justify-center">
                      {idx + 1}
                    </span>
                    <div>
                      <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                        {st.name}
                      </h4>
                      <p className="text-xs text-slate-400">
                        {st.sessions.toLocaleString()} sessions ({st.overall_conversion}% of all entries)
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs font-semibold text-emerald-600 dark:text-emerald-400">
                      {st.step_conversion}% retained
                    </div>
                    {idx > 0 && (
                      <div className="text-[11px] text-rose-500 font-medium">
                        -{st.drop_off_count.toLocaleString()} drop-offs ({st.drop_off_rate}%)
                      </div>
                    )}
                  </div>
                </div>
                {idx < data.stages.length - 1 && (
                  <div className="flex justify-center my-1">
                    <ArrowDown className="w-4 h-4 text-slate-400" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
