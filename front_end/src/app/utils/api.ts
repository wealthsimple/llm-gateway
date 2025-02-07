import { z } from 'zod';
import { API_BASE_URL, API_CREDENTIALS } from '../constants';

interface FetchOptions extends RequestInit {
  headers?: Record<string, string>;
}

export class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

export const fetchWithAuth = async <T>(
  endpoint: string,
  options: FetchOptions = {},
  schema?: z.ZodType<T>
): Promise<T> => {
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Basic ${btoa(`${API_CREDENTIALS.username}:${API_CREDENTIALS.password}`)}`
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    credentials: 'omit',
    headers: { ...headers, ...options.headers }
  });

  if (!response.ok) {
    throw new APIError(response.status, `HTTP error! status: ${response.status}`);
  }

  try {
    const contentType = response.headers.get('content-type');
    if (!contentType?.includes('application/json')) {
      throw new Error('Invalid response format: expected JSON');
    }
    const data = await response.json();

    if (schema) {
      return schema.parse(data);
    }
    return data;
  } catch (error) {
    if (error instanceof z.ZodError) {
      const validationError = new Error(`Invalid response format: ${error.message}`);
      validationError.name = 'ValidationError';
      throw validationError;
    }
    const parseError = new Error('Failed to parse JSON response');
    parseError.name = 'JSONParseError';
    throw parseError;
  }
};
