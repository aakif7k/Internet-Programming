import React, { useRef } from 'react';
import ReactECharts from 'echarts-for-react';

interface DynamicChartProps {
  option: Record<string, any>;
  height?: string | number;
  loading?: boolean;
  isDark?: boolean;
  className?: string;
}

export const DynamicChart: React.FC<DynamicChartProps> = ({
  option,
  height = '400px',
  loading = false,
  isDark = false,
  className = '',
}) => {
  const chartRef = useRef<any>(null);

  // Merge theme styling into option
  const themeAdjustedOption: Record<string, any> = {
    backgroundColor: 'transparent',
    textStyle: {
      color: isDark ? '#e2e8f0' : '#1e293b',
      fontFamily: 'Inter, system-ui, sans-serif',
    },
    toolbox: {
      show: true,
      feature: {
        saveAsImage: { show: true, title: 'Save Image', pixelRatio: 2 },
        restore: { show: true, title: 'Reset Zoom' },
        dataZoom: { show: true, title: { zoom: 'Box Zoom', back: 'Zoom Reset' } },
        dataView: { show: true, title: 'Data View', readOnly: true },
      },
      iconStyle: {
        borderColor: isDark ? '#cbd5e1' : '#475569',
      },
      right: 15,
      top: 5,
    },
    grid: {
      top: 50,
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true,
      ...option.grid,
    },
    ...option,
  };

  // Adjust Tooltip theme colors
  themeAdjustedOption.tooltip = {
    backgroundColor: isDark ? '#1e293b' : '#ffffff',
    borderColor: isDark ? '#334155' : '#cbd5e1',
    borderWidth: 1,
    textStyle: {
      color: isDark ? '#f8fafc' : '#0f172a',
      fontSize: 12,
    },
    ...themeAdjustedOption.tooltip,
  };

  // Adjust Legend labels
  if (themeAdjustedOption.legend) {
    const legends = Array.isArray(themeAdjustedOption.legend)
      ? themeAdjustedOption.legend
      : [themeAdjustedOption.legend];
    legends.forEach((lg: any) => {
      lg.textStyle = {
        color: isDark ? '#e2e8f0' : '#1e293b',
        fontSize: 12,
        ...lg.textStyle,
      };
    });
  }

  // Adjust Title text style
  if (themeAdjustedOption.title) {
    themeAdjustedOption.title.textStyle = {
      color: isDark ? '#f8fafc' : '#0f172a',
      ...themeAdjustedOption.title.textStyle,
    };
  }

  // Adjust xAxis and yAxis if present
  if (themeAdjustedOption.xAxis) {
    const axes = Array.isArray(themeAdjustedOption.xAxis) ? themeAdjustedOption.xAxis : [themeAdjustedOption.xAxis];
    axes.forEach((ax: any) => {
      ax.nameTextStyle = { color: isDark ? '#cbd5e1' : '#334155', fontWeight: 600, ...ax.nameTextStyle };
      ax.axisLine = { lineStyle: { color: isDark ? '#475569' : '#cbd5e1' } };
      ax.axisLabel = { color: isDark ? '#cbd5e1' : '#475569', ...ax.axisLabel };
      ax.splitLine = { lineStyle: { color: isDark ? '#334155' : '#f1f5f9' }, ...ax.splitLine };
    });
  }

  if (themeAdjustedOption.yAxis) {
    const axes = Array.isArray(themeAdjustedOption.yAxis) ? themeAdjustedOption.yAxis : [themeAdjustedOption.yAxis];
    axes.forEach((ax: any) => {
      ax.nameTextStyle = { color: isDark ? '#cbd5e1' : '#334155', fontWeight: 600, ...ax.nameTextStyle };
      ax.axisLine = { lineStyle: { color: isDark ? '#475569' : '#cbd5e1' } };
      ax.axisLabel = { color: isDark ? '#cbd5e1' : '#475569', ...ax.axisLabel };
      ax.splitLine = { lineStyle: { color: isDark ? '#334155' : '#f1f5f9' }, ...ax.splitLine };
    });
  }

  return (
    <div className={`w-full overflow-hidden ${className}`}>
      <ReactECharts
        ref={chartRef}
        option={themeAdjustedOption}
        style={{ height: height, width: '100%' }}
        showLoading={loading}
        loadingOption={{
          text: 'Loading Chart...',
          color: '#0c87eb',
          textColor: isDark ? '#f8fafc' : '#0f172a',
          maskColor: isDark ? 'rgba(15, 23, 42, 0.7)' : 'rgba(255, 255, 255, 0.7)',
        }}
        opts={{ renderer: 'canvas' }}
        notMerge={true}
      />
    </div>
  );
};
