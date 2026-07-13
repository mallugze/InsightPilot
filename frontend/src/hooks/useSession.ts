import { useState, useEffect } from 'react';
import { getOrCreateSessionId } from '../utils/storage';

export const useSession = () => {
  const [sessionId, setSessionId] = useState<string>('');

  useEffect(() => {
    const activeSessionId = getOrCreateSessionId();
    setSessionId(activeSessionId);
  }, []);

  return { sessionId };
};
