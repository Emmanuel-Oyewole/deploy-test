import axios from 'axios';
import authService from './authService';

const axiosAuth = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true, 
});

axiosAuth.interceptors.request.use(
  async (config) => {
    
    const token = document.cookie
      .split('; ')
      .find((row) => row.startsWith('access_token='))
      ?.split('=')[1];

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosAuth.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const newToken = await authService.refreshToken();
        document.cookie = `access_token=${newToken}; path=/; HttpOnly`;

        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
        return axiosAuth(originalRequest);
      } catch (err) {
        console.error('Failed to refresh token', err);
        
      }
    }

    return Promise.reject(error);
  }
);

export default axiosAuth;