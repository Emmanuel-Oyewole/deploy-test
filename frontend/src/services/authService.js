import axios from "axios";

const authService = {
  refreshToken: async () => {
    try {
      const response = await axios.post("/auth/refresh");
      return response.data.access_token;
    } catch (error) {
      console.error("Failed to refresh token", error);
      throw error;
    }
  },
};

export default authService;