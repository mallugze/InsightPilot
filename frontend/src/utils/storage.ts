export const STORAGE_KEYS = {
  SESSION_ID: 'insight_pilot_session_id',
} as const;

export const getSessionId = (): string | null => {
  try {
    return localStorage.getItem(STORAGE_KEYS.SESSION_ID);
  } catch (error) {
    console.error('Error accessing localStorage:', error);
    return null;
  }
};

export const setSessionId = (sessionId: string): void => {
  try {
    localStorage.setItem(STORAGE_KEYS.SESSION_ID, sessionId);
  } catch (error) {
    console.error('Error setting localStorage:', error);
  }
};

export const generateUUID = (): string => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
};

export const getOrCreateSessionId = (): string => {
  let sessionId = getSessionId();
  if (!sessionId) {
    sessionId = generateUUID();
    setSessionId(sessionId);
  }
  return sessionId;
};
