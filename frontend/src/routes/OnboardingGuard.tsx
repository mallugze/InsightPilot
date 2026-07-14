import { Navigate, useLocation } from 'react-router-dom';
import { useWorkspace } from '../context/WorkspaceContext';

interface GuardProps {
  children: React.ReactNode;
}

export const OnboardingGuard = ({ children }: GuardProps) => {
  const { profile, isSessionResumed, uploadState, analysisState, isWorkspaceConfirmed } = useWorkspace();
  const location = useLocation();
  const path = location.pathname;

  // 1. Profile registration check
  if (!profile || !profile.fullName) {
    if (path !== '/welcome') {
      return <Navigate to="/welcome" replace />;
    }
    return <>{children}</>;
  }

  // If user is at /welcome but profile is set, redirect to next step
  if (path === '/welcome') {
    return <Navigate to="/upload" replace />;
  }

  // 2. Welcome back resumption check for fully onboarded returning sessions
  if (isWorkspaceConfirmed && !isSessionResumed) {
    if (path !== '/welcome-back') {
      return <Navigate to="/welcome-back" replace />;
    }
    return <>{children}</>;
  }

  // If session is already resumed and they try to load /welcome-back, go to dashboard
  if (isWorkspaceConfirmed && isSessionResumed && path === '/welcome-back') {
    return <Navigate to="/dashboard" replace />;
  }

  // 3. File upload check
  if (!isWorkspaceConfirmed && !uploadState) {
    if (path !== '/upload') {
      return <Navigate to="/upload" replace />;
    }
    return <>{children}</>;
  }

  // 4. Analyzing progress check
  if (!isWorkspaceConfirmed && analysisState === 'analyzing') {
    if (path !== '/analysis-progress') {
      return <Navigate to="/analysis-progress" replace />;
    }
    return <>{children}</>;
  }

  // 5. Analysis success and workspace name review checks
  if (!isWorkspaceConfirmed && analysisState === 'completed') {
    if (path !== '/analysis-success' && path !== '/review-analysis') {
      return <Navigate to="/analysis-success" replace />;
    }
    return <>{children}</>;
  }

  // 6. Fully completed session redirects away from onboarding flow
  const isOnboardingUrl = ['/welcome', '/welcome-back', '/upload', '/analysis-progress', '/analysis-success', '/review-analysis'].includes(path);
  if (isWorkspaceConfirmed && isSessionResumed && isOnboardingUrl) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};
