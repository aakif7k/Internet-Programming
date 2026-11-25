import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  badge?: string;
  badgeColor?: 'green' | 'blue' | 'purple' | 'amber';
  loading?: boolean;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  badge,
  badgeColor = 'blue',
  loading = false,
}) => {
  const badgeClasses = {
    green: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800',
    blue: 'bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-400 border border-blue-200 dark:border-blue-800',
    purple: 'bg-purple-50 text-purple-700 dark:bg-purple-950/60 dark:text-purple-400 border border-purple-200 dark:border-purple-800',
    amber: 'bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400 border border-amber-200 dark:border-amber-800',
  }[badgeColor];

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-xl p-5 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          {title}
        </span>
        <div className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <div className="mt-2 flex items-baseline justify-between">
        {loading ? (
          <div className="h-8 w-24 bg-slate-200 dark:bg-slate-700 animate-pulse rounded" />
        ) : (
          <div className="text-2xl font-bold text-slate-900 dark:text-slate-50">{value}</div>
        )}
        {badge && (
          <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${badgeClasses}`}>
            {badge}
          </span>
        )}
      </div>
      {subtitle && (
        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">{subtitle}</p>
      )}
    </div>
  );
};
