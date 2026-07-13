import { getOrCreateSessionId } from '../utils/storage';

const API_BASE_URL = 'http://localhost:8000/api';

interface RequestOptions extends RequestInit {
  params?: Record<string, string>;
}

export const apiFetch = async <T>(endpoint: string, options: RequestOptions = {}): Promise<T> => {
  const sessionId = getOrCreateSessionId();
  
  const headers = new Headers(options.headers);
  headers.set('X-Session-ID', sessionId);
  if (!(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  let url = `${API_BASE_URL}${endpoint}`;
  if (options.params) {
    const searchParams = new URLSearchParams(options.params);
    url += `?${searchParams.toString()}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `API error: ${response.statusText}`);
  }

  return response.json() as Promise<T>;
};
