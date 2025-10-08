/**
 * API configuration that automatically switches between local and production.
 * 
 * Priority:
 * 1. Environment variable REACT_APP_API_URL (if set)
 * 2. Auto-detect based on hostname:
 *    - localhost -> http://localhost:8000
 *    - production -> https://boot-lang-gscvbveeg3dvgefh.eastus2-01.azurewebsites.net
 */

const getApiUrl = (): string => {
  // 1. Check for environment variable override
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // 2. Auto-detect based on hostname
  const hostname = window.location.hostname;
  
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    // Local development
    return 'http://localhost:8000';
  }
  
  // Production: Azure deployment
  return 'https://boot-lang-gscvbveeg3dvgefh.eastus2-01.azurewebsites.net';
};

export const API_URL = getApiUrl();

