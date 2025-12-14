// frontend/src/utils/axiosInstance.js

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create a configured instance of Axios
const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 💥 CRITICAL INTERCEPTOR ADDITION 💥
// This intercepts every request before it is sent to the server.
axiosInstance.interceptors.request.use(
    (config) => {
        // Retrieve the token from Local Storage on every request.
        // This ensures the token is present even if the component loads before the AuthContext useEffect runs.
        const token = localStorage.getItem('jwt_token');

        if (token) {
            // Set the Authorization header if the token exists
            config.headers.Authorization = `Bearer ${token}`;
        } else {
            // Ensure no header is sent if the token is missing/cleared
            delete config.headers.Authorization;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default axiosInstance;