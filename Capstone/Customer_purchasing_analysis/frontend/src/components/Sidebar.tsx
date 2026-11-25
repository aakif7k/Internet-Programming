import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  UploadCloud,
  SlidersHorizontal,
  BarChart3,
  MousePointerClick,
  ShoppingBag,
  Filter,
  Users2,
  BrainCircuit,
  DollarSign,
  TrendingUp,
  Palette,
  ChevronLeft,
  ChevronRight,
  Database
} from 'lucide-react';

interface SidebarProps {
  collapsed: boolean;
  setCollapsed: (collapsed: boolean) => void;
  datasetStatus?: string | null;
}

const navItems = [
  { path: '/', label: 'Overview', icon: LayoutDashboard },
  { path: '/upload', label: 'Dataset Upload', icon: UploadCloud },
  { path: '/preprocessing', label: 'Preprocessing', icon: SlidersHorizontal },
  { path: '/clickstream', label: 'Clickstream Analytics', icon: MousePointerClick },
  { path: '/purchase-patterns', label: 'Purchase Patterns', icon: ShoppingBag },
  { path: '/funnel', label: 'Conversion Funnel', icon: Filter },
  { path: '/segmentation', label: 'Segmentation (RFM)', icon: Users2 },
  { path: '/conversion-prediction', label: 'Conversion Prediction', icon: BrainCircuit, badge: 'ML' },
  { path: '/revenue-estimation', label: 'Revenue Estimation', icon: DollarSign, badge: 'ML' },
  { path: '/time-series', label: 'Time-Series Forecast', icon: TrendingUp },
  { path: '/visual-studio', label: 'Visual Studio', icon: Palette, badge: 'R-viz' },
];

export const Sidebar: React.FC<SidebarProps> = ({ collapsed, setCollapsed, datasetStatus }) => {
  return (
    <aside
      className={`fixed top-0 left-0 z-40 h-screen transition-all duration-300 ease-in-out bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col ${
        collapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* Brand Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-slate-200 dark:border-slate-800">
        {!collapsed && (
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-sm shadow">
              R
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-sm text-slate-800 dark:text-slate-100 tracking-tight leading-tight">
                Clickstream ML
              </span>
              <span className="text-[10px] text-slate-400 dark:text-slate-500 uppercase font-medium">
                R Analytics Capstone
              </span>
            </div>
          </div>
        )}
        {collapsed && (
          <div className="mx-auto w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-sm shadow">
            R
          </div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          title={collapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Dataset Status Pill */}
      {!collapsed && (
        <div className="px-4 py-2.5 mx-3 mt-3 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/50 flex items-center space-x-2">
          <Database className={`w-3.5 h-3.5 ${datasetStatus ? 'text-emerald-500' : 'text-amber-500'}`} />
          <div className="flex flex-col">
            <span className="text-[10px] uppercase font-semibold text-slate-400">Data Engine</span>
            <span className="text-xs font-medium text-slate-700 dark:text-slate-300 truncate max-w-[170px]">
              {datasetStatus ? `Active (${datasetStatus})` : 'No data loaded'}
            </span>
          </div>
        </div>
      )}

      {/* Nav List */}
      <nav className="flex-1 overflow-y-auto px-3 py-3 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors group ${
                isActive
                  ? 'bg-blue-50 text-blue-700 dark:bg-blue-950/70 dark:text-blue-400 shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`
            }
            title={collapsed ? item.label : undefined}
          >
            <item.icon className="w-5 h-5 shrink-0" />
            {!collapsed && (
              <span className="ml-3 flex-1 truncate">{item.label}</span>
            )}
            {!collapsed && item.badge && (
              <span className="ml-auto text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-blue-100 text-blue-700 dark:bg-blue-900/60 dark:text-blue-300">
                {item.badge}
              </span>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Bottom Footer Info */}
      {!collapsed && (
        <div className="p-3 border-t border-slate-200 dark:border-slate-800 text-[11px] text-slate-400 text-center">
          R + FastAPI + React Vite
        </div>
      )}
    </aside>
  );
};
