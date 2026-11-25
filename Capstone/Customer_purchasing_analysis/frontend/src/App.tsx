import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { api } from './api/client';
import { HealthResponse, DatasetStatus } from './types';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';

import { Overview } from './pages/Overview';
import { DatasetUpload } from './pages/DatasetUpload';
import { DataPreprocessing } from './pages/DataPreprocessing';
import { ClickstreamAnalysis } from './pages/ClickstreamAnalysis';
import { PurchasePatterns } from './pages/PurchasePatterns';
import { ConversionFunnel } from './pages/ConversionFunnel';
import { CustomerSegmentation } from './pages/CustomerSegmentation';
import { ConversionPrediction } from './pages/ConversionPrediction';
import { RevenueEstimation } from './pages/RevenueEstimation';
import { TimeSeries } from './pages/TimeSeries';
import { VisualAnalyticsStudio } from './pages/VisualAnalyticsStudio';

export const App: React.FC = () => {
  const [isDark, setIsDark] = useState<boolean>(() => {
    return localStorage.getItem('theme') === 'dark' ||
      (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });
  const [collapsed, setCollapsed] = useState(false);
  const [datasetStatus, setDatasetStatus] = useState<DatasetStatus | null>(null);
  const [loadingAction, setLoadingAction] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDark]);

  const fetchHealthAndStatus = async () => {
    try {
      const resp = await api.get<HealthResponse>('/health');
      setDatasetStatus(resp.data.dataset_status);
    } catch (err) {
      console.error('Health check failed:', err);
    }
  };

  useEffect(() => {
    fetchHealthAndStatus();
  }, []);

  const handleLoadDefault = async () => {
    setLoadingAction(true);
    try {
      await api.post('/dataset/load-default');
      await fetchHealthAndStatus();
    } catch (err) {
      console.error('Failed to load default dataset:', err);
    } finally {
      setLoadingAction(false);
    }
  };

  const handleClearDataset = async () => {
    if (!confirm('Are you sure you want to clear the session dataset?')) return;
    setLoadingAction(true);
    try {
      await api.delete('/dataset/clear');
      await fetchHealthAndStatus();
    } catch (err) {
      console.error('Failed to clear dataset:', err);
    } finally {
      setLoadingAction(false);
    }
  };

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex">
        {/* Navigation Sidebar */}
        <Sidebar
          collapsed={collapsed}
          setCollapsed={setCollapsed}
          datasetStatus={datasetStatus?.active_file}
        />

        {/* Main Content Area */}
        <div
          className={`flex-1 flex flex-col min-h-screen transition-all duration-300 ease-in-out ${
            collapsed ? 'ml-20' : 'ml-64'
          }`}
        >
          <Header
            collapsed={collapsed}
            isDark={isDark}
            toggleDarkMode={() => setIsDark(!isDark)}
            datasetStatus={datasetStatus}
            onLoadDefault={handleLoadDefault}
            onClearDataset={handleClearDataset}
            loadingAction={loadingAction}
          />

          <main className="flex-1 p-6 md:p-8 mt-16 max-w-7xl w-full mx-auto">
            <Routes>
              <Route path="/" element={<Overview isDark={isDark} onLoadDefault={handleLoadDefault} />} />
              <Route
                path="/upload"
                element={
                  <DatasetUpload
                    onDatasetChanged={fetchHealthAndStatus}
                    onLoadDefault={handleLoadDefault}
                    loadingAction={loadingAction}
                  />
                }
              />
              <Route
                path="/preprocessing"
                element={<DataPreprocessing onCleanedReady={fetchHealthAndStatus} />}
              />
              <Route
                path="/clickstream"
                element={<ClickstreamAnalysis isDark={isDark} onLoadDefault={handleLoadDefault} />}
              />
              <Route
                path="/purchase-patterns"
                element={<PurchasePatterns isDark={isDark} onLoadDefault={handleLoadDefault} />}
              />
              <Route
                path="/funnel"
                element={<ConversionFunnel isDark={isDark} onLoadDefault={handleLoadDefault} datasetStatus={datasetStatus} />}
              />
              <Route
                path="/segmentation"
                element={<CustomerSegmentation isDark={isDark} onLoadDefault={handleLoadDefault} />}
              />
              <Route
                path="/conversion-prediction"
                element={
                  <ConversionPrediction
                    isDark={isDark}
                    onLoadDefault={handleLoadDefault}
                    datasetStatus={datasetStatus}
                  />
                }
              />
              <Route
                path="/revenue-estimation"
                element={
                  <RevenueEstimation
                    isDark={isDark}
                    onLoadDefault={handleLoadDefault}
                    datasetStatus={datasetStatus}
                  />
                }
              />
              <Route
                path="/time-series"
                element={<TimeSeries isDark={isDark} onLoadDefault={handleLoadDefault} />}
              />
              <Route
                path="/visual-studio"
                element={
                  <VisualAnalyticsStudio
                    isDark={isDark}
                    onLoadDefault={handleLoadDefault}
                    datasetStatus={datasetStatus}
                  />
                }
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
};
