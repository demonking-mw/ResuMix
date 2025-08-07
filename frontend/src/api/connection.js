import axios from "axios";

// Set your backend API base URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

console.log("🔍 Frontend debugging:");
console.log("VITE_API_BASE_URL from env:", import.meta.env.VITE_API_BASE_URL);
console.log("Final API_BASE_URL used:", API_BASE_URL);
console.log("All env vars:", import.meta.env);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    console.log("🚀 Making API request:");
    console.log("  URL:", config.baseURL + config.url);
    console.log("  Method:", config.method);
    console.log("  Params:", config.params);
    console.log("  Data:", config.data);
    
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error("❌ Request error:", error);
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => {
    console.log("✅ API response success:");
    console.log("  Status:", response.status);
    console.log("  Data:", response.data);
    return response;
  },
  (error) => {
    console.error("❌ API response error:");
    console.error("  Status:", error.response?.status);
    console.error("  Data:", error.response?.data);
    console.error("  URL:", error.config?.url);
    console.error("  Full error:", error);
    
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('authToken');
      localStorage.removeItem('reauthToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Helper function to make reauth requests (for when you need to use the reauth token)
export const makeReauthRequest = async (url, data = {}, method = 'GET') => {
  const reauthToken = localStorage.getItem('reauthToken');
  const authToken = localStorage.getItem('authToken');
  
  if (!reauthToken || !authToken) {
    throw new Error('No reauth token available');
  }

  // Decode the auth token to get the user ID
  try {
    const decodedToken = JSON.parse(atob(authToken.split('.')[1]));
    const uid = decodedToken.sub || decodedToken.user_id || decodedToken.uid;
    
    const requestData = {
      ...data,
      type: 're',
      uid: uid,
      reauth_jwt: reauthToken
    };

    if (method.toLowerCase() === 'post') {
      return await api.post(url, requestData);
    } else if (method.toLowerCase() === 'get') {
      return await api.get(url, { params: requestData });
    } else {
      return await api.request({
        method: method,
        url: url,
        data: requestData
      });
    }
  } catch (error) {
    console.error('Error making reauth request:', error);
    throw error;
  }
};

export default api;
