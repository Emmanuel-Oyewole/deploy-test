import axios from 'axios';

const axiosLogin = axios.create({
    withCredentials: true,
    baseURL: 'http://localhost:8000', // Replace with your API base URL
    headers: {
        'Content-Type': 'application/json',
    },
});

export default axiosLogin;