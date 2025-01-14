import { useEffect } from 'react';
import apiClient from '../services/apiClient'

function useTokenRefresh() {
    useEffect(() => {
        const refreshToken = async () => {
            try {
                await apiClient.post('/refresh-token', {}, { withCredentials: true });
            } catch (error) {
                console.error('Token refresh failed', error);
            }
        };

        //Refresh 1 minute before the access token is expected to expire
        const interval = setInterval(refreshToken, 29 * 60 * 1000); // for a 30-minute expiry
        return () => clearInterval(interval);  // cleanup function to stop the interval when component unmounts

    }, []);
}

export default useTokenRefresh;