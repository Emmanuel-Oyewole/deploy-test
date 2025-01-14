import  { useState } from "react";
import axiosLogin from "../../services/axiosLogin";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [errorMessage, setErrorMessage] = useState(""); // Error handling

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Create URLSearchParams object
      const payload = new URLSearchParams();
      payload.append("username", formData.email);
      payload.append("password", formData.password);

      const response = await axiosLogin.post(
        "/auth/login",
        payload,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      console.log(response);

      if (response.status === 200) {
        const { id, access_token, refresh_token } = response.data;
        console.log("User ID:", id);
        console.log("Access Token:", access_token);
        console.log("Refresh Token:", refresh_token);
        setFormData({
          email: "",
          password: "",
        });

        // Store tokens securely (in localStorage or secure cookies)
        document.cookie = `token=${access_token}; path=/`;
        localStorage.setItem("refresh_token", refresh_token);
        console.log(document.cookie);

        // Decode the JWT token to get the user's role
        const decodedToken = jwtDecode(access_token);
        console.log("Decoded Token:", decodedToken);
        const userRole = decodedToken.role;
        console.log("User Role:", userRole);

        // Redirect user to the appropriate dashboard based on their role
        if (userRole === "Admin") {
          navigate("/admin");
        } else if (userRole === "Teacher") {
          navigate("/teacher");
        } else if (userRole === "Student") {
          navigate("/studentdashboard");
        } else {
          navigate("/login"); // Redirect to login if role is not recognized
        }
      } else {
        setErrorMessage("Invalid email or password.");
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage(
        error.response?.data?.detail || "An error occurred during login."
      );
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-primary">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-semibold text-primary mb-6">Login</h2>

        {errorMessage && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
            {errorMessage}
          </div>
        )}

        <div className="mb-4">
          <label htmlFor="email" className="block text-primary mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-primary"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="password" className="block text-primary mb-2">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-primary"
          />
        </div>

        <div className="mb-4 flex justify-between text-sm">
          <a
            href="/forgot-password"
            className="text-primary hover:text-blue-600"
          >
            Forgot Password?
          </a>
          <a href="/enrol" className="text-primary hover:text-blue-600">
            Don&apos;t have an account? Enrol
          </a>
        </div>

        <button
          type="submit"
          className="w-full py-2 bg-primary text-white font-semibold rounded-md hover:bg-blue-800 focus:outline-none"
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default LoginPage;