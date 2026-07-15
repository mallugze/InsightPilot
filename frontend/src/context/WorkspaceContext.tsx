import { createContext, useContext, useState } from 'react';

export interface UserProfile {
  fullName: string;
  email: string;
  companyName?: string;
  memberSince: string;
}

export interface DatasetUploadState {
  fileName: string;
  fileSize: string;
  datasetId?: string;
  datasetType?: string;
  rowsCount?: number;
  colsCount?: number;
  businessPulse?: number;
  topInsight?: string;
  missingValues?: number;
  duplicates?: number;
  qualityScore?: number;
  preview?: any[];
  columnMetadata?: any;
}

export interface AppNotification {
  id: string;
  title: string;
  description: string;
  type: 'info' | 'success' | 'warning';
  read: boolean;
  timestamp: string;
}

export type AnalysisState = 'idle' | 'analyzing' | 'completed';

interface WorkspaceContextType {
  profile: UserProfile | null;
  isEmailVerified: boolean;
  isSessionResumed: boolean;
  uploadState: DatasetUploadState | null;
  analysisState: AnalysisState;
  workspaceName: string | null;
  isWorkspaceConfirmed: boolean;
  notifications: AppNotification[];
  saveProfile: (fullName: string, email: string, companyName?: string) => void;
  verifyEmailCode: (code: string) => Promise<boolean>;
  setSessionResumed: (resumed: boolean) => void;
  startUpload: (uploadData: DatasetUploadState) => void;
  completeAnalysis: (
    datasetType: string,
    rowsCount: number,
    colsCount: number,
    businessPulse: number,
    topInsight: string,
    suggestedWorkspaceName: string
  ) => void;
  confirmWorkspace: (name: string) => void;
  resetOnboarding: () => void;
  resetOnboardingKeepProfile: () => void;
  addNotification: (title: string, description: string, type: 'info' | 'success' | 'warning') => void;
  markNotificationsAsRead: () => void;
  dismissNotification: (id: string) => void;
}

const WorkspaceContext = createContext<WorkspaceContextType | undefined>(undefined);

const LOCAL_STORAGE_KEYS = {
  PROFILE: 'insightpilot_user_profile',
  EMAIL_VERIFIED: 'insightpilot_email_verified',
  UPLOAD_STATE: 'insightpilot_upload_state',
  ANALYSIS_STATE: 'insightpilot_analysis_state',
  WORKSPACE_NAME: 'insightpilot_workspace_name',
  WORKSPACE_CONFIRMED: 'insightpilot_workspace_confirmed',
  NOTIFICATIONS: 'insightpilot_notifications',
};

const SESSION_STORAGE_KEYS = {
  SESSION_RESUMED: 'insightpilot_session_resumed',
};

export const WorkspaceProvider = ({ children }: { children: React.ReactNode }) => {
  const [profile, setProfile] = useState<UserProfile | null>(() => {
    const raw = localStorage.getItem(LOCAL_STORAGE_KEYS.PROFILE);
    return raw ? JSON.parse(raw) : null;
  });

  const [isEmailVerified, setIsEmailVerified] = useState<boolean>(() => {
    return localStorage.getItem(LOCAL_STORAGE_KEYS.EMAIL_VERIFIED) === 'true';
  });

  const [isSessionResumed, setIsSessionResumedState] = useState<boolean>(() => {
    return sessionStorage.getItem(SESSION_STORAGE_KEYS.SESSION_RESUMED) === 'true';
  });

  const [uploadState, setUploadState] = useState<DatasetUploadState | null>(() => {
    const raw = localStorage.getItem(LOCAL_STORAGE_KEYS.UPLOAD_STATE);
    return raw ? JSON.parse(raw) : null;
  });

  const [analysisState, setAnalysisState] = useState<AnalysisState>(() => {
    return (localStorage.getItem(LOCAL_STORAGE_KEYS.ANALYSIS_STATE) as AnalysisState) || 'idle';
  });

  const [workspaceName, setWorkspaceName] = useState<string | null>(() => {
    return localStorage.getItem(LOCAL_STORAGE_KEYS.WORKSPACE_NAME);
  });

  const [isWorkspaceConfirmed, setIsWorkspaceConfirmed] = useState<boolean>(() => {
    return localStorage.getItem(LOCAL_STORAGE_KEYS.WORKSPACE_CONFIRMED) === 'true';
  });

  const [notifications, setNotifications] = useState<AppNotification[]>(() => {
    const raw = localStorage.getItem(LOCAL_STORAGE_KEYS.NOTIFICATIONS);
    return raw ? JSON.parse(raw) : [
      {
        id: 'welcome-notif',
        title: 'System Active',
        description: 'InsightPilot Decision intelligence platform active.',
        type: 'info',
        read: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }
    ];
  });

  const addNotification = (title: string, description: string, type: 'info' | 'success' | 'warning') => {
    const newNotif: AppNotification = {
      id: Math.random().toString(36).substr(2, 9),
      title,
      description,
      type,
      read: false,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setNotifications(prev => {
      const updated = [newNotif, ...prev];
      localStorage.setItem(LOCAL_STORAGE_KEYS.NOTIFICATIONS, JSON.stringify(updated));
      return updated;
    });
  };

  const markNotificationsAsRead = () => {
    setNotifications(prev => {
      const updated = prev.map(n => ({ ...n, read: true }));
      localStorage.setItem(LOCAL_STORAGE_KEYS.NOTIFICATIONS, JSON.stringify(updated));
      return updated;
    });
  };

  const dismissNotification = (id: string) => {
    setNotifications(prev => {
      const updated = prev.filter(n => n.id !== id);
      localStorage.setItem(LOCAL_STORAGE_KEYS.NOTIFICATIONS, JSON.stringify(updated));
      return updated;
    });
  };

  const saveProfile = (fullName: string, email: string, companyName?: string) => {
    const memberSince = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    const newProfile = { fullName, email, companyName, memberSince };
    setProfile(newProfile);
    setIsEmailVerified(false); // Reset verified status on new profile registration
    localStorage.setItem(LOCAL_STORAGE_KEYS.PROFILE, JSON.stringify(newProfile));
    localStorage.setItem(LOCAL_STORAGE_KEYS.EMAIL_VERIFIED, 'false');
    addNotification('Account Created', 'Successfully registered user profile.', 'success');
  };

  const verifyEmailCode = async (code: string): Promise<boolean> => {
    // Stub email code validation (accepts any 6 digit code for MVP)
    if (code.trim().length === 6) {
      setIsEmailVerified(true);
      localStorage.setItem(LOCAL_STORAGE_KEYS.EMAIL_VERIFIED, 'true');
      addNotification('Email Verified', 'Your email address has been successfully verified.', 'success');
      return true;
    }
    return false;
  };

  const setSessionResumed = (resumed: boolean) => {
    setIsSessionResumedState(resumed);
    sessionStorage.setItem(SESSION_STORAGE_KEYS.SESSION_RESUMED, resumed ? 'true' : 'false');
  };

  const startUpload = (uploadData: DatasetUploadState) => {
    setUploadState(uploadData);
    setAnalysisState('analyzing');
    localStorage.setItem(LOCAL_STORAGE_KEYS.UPLOAD_STATE, JSON.stringify(uploadData));
    localStorage.setItem(LOCAL_STORAGE_KEYS.ANALYSIS_STATE, 'analyzing');
    addNotification('File Ingested', `Dataset ${uploadData.fileName} processed successfully.`, 'info');
  };

  const completeAnalysis = (
    datasetType: string,
    rowsCount: number,
    colsCount: number,
    businessPulse: number,
    topInsight: string,
    suggestedWorkspaceName: string
  ) => {
    if (uploadState) {
      const updatedState: DatasetUploadState = {
        ...uploadState,
        datasetType,
        rowsCount,
        colsCount,
        businessPulse,
        topInsight,
      };
      setUploadState(updatedState);
      localStorage.setItem(LOCAL_STORAGE_KEYS.UPLOAD_STATE, JSON.stringify(updatedState));
    }
    setAnalysisState('completed');
    setWorkspaceName(suggestedWorkspaceName);
    localStorage.setItem(LOCAL_STORAGE_KEYS.ANALYSIS_STATE, 'completed');
    localStorage.setItem(LOCAL_STORAGE_KEYS.WORKSPACE_NAME, suggestedWorkspaceName);
    addNotification('Analysis Completed', 'AI recommendations and Business Pulse metrics are ready.', 'success');
  };

  const confirmWorkspace = (name: string) => {
    setWorkspaceName(name);
    setIsWorkspaceConfirmed(true);
    localStorage.setItem(LOCAL_STORAGE_KEYS.WORKSPACE_NAME, name);
    localStorage.setItem(LOCAL_STORAGE_KEYS.WORKSPACE_CONFIRMED, 'true');
    addNotification('Workspace Activated', `Active environment shifted to ${name}.`, 'success');
  };

  const resetOnboarding = () => {
    setProfile(null);
    setIsEmailVerified(false);
    setUploadState(null);
    setAnalysisState('idle');
    setWorkspaceName(null);
    setIsWorkspaceConfirmed(false);
    setSessionResumed(false);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.PROFILE);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.EMAIL_VERIFIED);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.UPLOAD_STATE);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.ANALYSIS_STATE);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.WORKSPACE_NAME);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.WORKSPACE_CONFIRMED);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.NOTIFICATIONS);
    sessionStorage.removeItem(SESSION_STORAGE_KEYS.SESSION_RESUMED);
  };

  const resetOnboardingKeepProfile = () => {
    setUploadState(null);
    setAnalysisState('idle');
    setWorkspaceName(null);
    setIsWorkspaceConfirmed(false);
    setSessionResumed(true); // Don't trigger welcome back again since they just chose to start fresh
    localStorage.removeItem(LOCAL_STORAGE_KEYS.UPLOAD_STATE);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.ANALYSIS_STATE);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.WORKSPACE_NAME);
    localStorage.removeItem(LOCAL_STORAGE_KEYS.WORKSPACE_CONFIRMED);
    addNotification('New Workspace Initiated', 'Previous dataset context cleared.', 'info');
  };

  return (
    <WorkspaceContext.Provider
      value={{
        profile,
        isEmailVerified,
        isSessionResumed,
        uploadState,
        analysisState,
        workspaceName,
        isWorkspaceConfirmed,
        notifications,
        saveProfile,
        verifyEmailCode,
        setSessionResumed,
        startUpload,
        completeAnalysis,
        confirmWorkspace,
        resetOnboarding,
        resetOnboardingKeepProfile,
        addNotification,
        markNotificationsAsRead,
        dismissNotification,
      }}
    >
      {children}
    </WorkspaceContext.Provider>
  );
};

export const useWorkspace = () => {
  const context = useContext(WorkspaceContext);
  if (context === undefined) {
    throw new Error('useWorkspace must be used within a WorkspaceProvider');
  }
  return context;
};
