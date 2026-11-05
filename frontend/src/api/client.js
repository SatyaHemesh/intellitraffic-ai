// frontend/src/api/client.js
import axios from 'axios';

const apiClient = axios.create({
  // In Vite, this targets the proxy set up in vite.config.js, routing to FastAPI port 8000
  baseURL: '/api', 
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor for handling errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data?.message || error.message);
    return Promise.reject(error);
  }
);

export default apiClient;