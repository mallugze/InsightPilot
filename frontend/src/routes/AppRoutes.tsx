import { Routes, Route } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import LandingPage from '../features/landing/pages/LandingPage';
import DashboardPage from '../features/dashboard/pages/DashboardPage';
import UploadPage from '../features/upload/pages/UploadPage';
import ChatPage from '../features/chat/pages/ChatPage';
import ReportsPage from '../features/reports/pages/ReportsPage';
import AnalysisHistoryPage from '../features/history/pages/AnalysisHistoryPage';

export const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Landing Page Route */}
      <Route path="/" element={<LandingPage />} />

      {/* Authenticated Workspace App Layout Routes */}
      <Route path="/dashboard" element={<Layout />}>
        <Route index element={<DashboardPage />} />
      </Route>
      
      <Route path="/" element={<Layout />}>
        <Route path="upload" element={<UploadPage />} />
        <Route path="chat" element={<ChatPage />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="history" element={<AnalysisHistoryPage />} />
        <Route
          path="settings"
          element={
            <div className="space-y-6 text-left">
              <div>
                <h1 className="text-3xl font-bold text-slate-900 m-0">Settings</h1>
                <p className="text-slate-500 mt-1">Configure your local workspace details and credentials.</p>
              </div>
              <div className="bg-white rounded-xl p-8 border border-slate-200 shadow-sm text-slate-600 text-sm">
                <p>System configurations are managed inside the backend environment variables.</p>
              </div>
            </div>
          }
        />
        <Route
          path="*"
          element={
            <div className="text-center py-20">
              <h2 className="text-2xl font-bold text-slate-800">404 - Page Not Found</h2>
              <p className="text-slate-500 mt-2">The route you requested does not exist.</p>
            </div>
          }
        />
      </Route>
    </Routes>
  );
};
