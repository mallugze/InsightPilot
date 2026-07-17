import { Routes, Route } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import { OnboardingGuard } from './OnboardingGuard';
import LandingPage from '../features/landing/pages/LandingPage';
import WelcomePage from '../features/onboarding/pages/WelcomePage';
import WelcomeBackPage from '../features/onboarding/pages/WelcomeBackPage';
import AnalysisProgressPage from '../features/onboarding/pages/AnalysisProgressPage';
import AnalysisSuccessPage from '../features/onboarding/pages/AnalysisSuccessPage';
import ReviewAnalysisPage from '../features/onboarding/pages/ReviewAnalysisPage';
import DashboardPage from '../features/dashboard/pages/DashboardPage';
import UploadPage from '../features/upload/pages/UploadPage';
import ChatPage from '../features/chat/pages/ChatPage';
import ReportsPage from '../features/reports/pages/ReportsPage';
import AnalysisHistoryPage from '../features/history/pages/AnalysisHistoryPage';
import WorkspacesPage from '../features/workspace/pages/WorkspacesPage';
import ProfilePage from '../features/profile/pages/ProfilePage';
import SettingsPage from '../features/profile/pages/SettingsPage';

export const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Landing Page Route */}
      <Route path="/" element={<LandingPage />} />

      {/* Onboarding Flow Screens */}
      <Route
        path="/welcome"
        element={
          <OnboardingGuard>
            <WelcomePage />
          </OnboardingGuard>
        }
      />
      <Route
        path="/welcome-back"
        element={
          <OnboardingGuard>
            <WelcomeBackPage />
          </OnboardingGuard>
        }
      />
      <Route
        path="/analysis-progress"
        element={
          <OnboardingGuard>
            <AnalysisProgressPage />
          </OnboardingGuard>
        }
      />
      <Route
        path="/analysis-success"
        element={
          <OnboardingGuard>
            <AnalysisSuccessPage />
          </OnboardingGuard>
        }
      />
      <Route
        path="/review-analysis"
        element={
          <OnboardingGuard>
            <ReviewAnalysisPage />
          </OnboardingGuard>
        }
      />

      {/* Authenticated Workspace App Layout Routes */}
      <Route
        path="/dashboard"
        element={
          <OnboardingGuard>
            <Layout />
          </OnboardingGuard>
        }
      >
        <Route index element={<DashboardPage />} />
      </Route>
      
      <Route
        path="/"
        element={
          <OnboardingGuard>
            <Layout />
          </OnboardingGuard>
        }
      >
        <Route path="upload" element={<UploadPage />} />
        <Route path="workspaces" element={<WorkspacesPage />} />
        {/* AI Ingestion Analyst Routes */}
        <Route path="chat" element={<ChatPage />} />
        <Route path="ai-analyst" element={<ChatPage />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="history" element={<AnalysisHistoryPage />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route path="settings" element={<SettingsPage />} />
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
