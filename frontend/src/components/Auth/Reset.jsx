import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useLocation } from "react-router-dom";

const ResetPasswordPage = () => {
  const [email, setEmail] = useState("");
  const [resetToken, setResetToken] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Get email and token from URL query parameters
    const queryParams = new URLSearchParams(location.search);
    const emailFromUrl = queryParams.get("email");
    const tokenFromUrl = queryParams.get("token");

    if (emailFromUrl) {
      setEmail(emailFromUrl);
    }
    if (tokenFromUrl) {
      setResetToken(tokenFromUrl);
    }
  }, [location]);

  const handleChange = (e) => {
    setNewPassword(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        token: resetToken,
        new_password: newPassword,
      }

      const response = await axios.post(
        "http://localhost:8000/auth/reset-password", // Update this URL to your API endpoint
        payload,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        setSuccessMessage("Your password has been successfully reset.");
        setEmail("");
        setResetToken("");
        setNewPassword("");
        setTimeout(() => {
          navigate("/login"); // Redirect to login page after success
        }, 2000);
      } else {
        setErrorMessage("An error occurred. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);

      // Handle backend errors
      if (error.response) {
        setErrorMessage(
          error.response.data.message ||
            "An error occurred during the reset process."
        );
      } else {
        setErrorMessage("An error occurred. Please try again later.");
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-primary">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-semibold text-primary mb-6">
          Reset Password
        </h2>

        {errorMessage && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
            {errorMessage}
          </div>
        )}

        {successMessage && (
          <div className="mb-4 p-3 bg-green-100 text-green-700 rounded-md">
            {successMessage}
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
            value={email}
            required
            readOnly
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-primary bg-gray-100"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="newPassword" className="block text-primary mb-2">
            New Password
          </label>
          <input
            type="password"
            id="newPassword"
            name="newPassword"
            value={newPassword}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-primary"
          />
        </div>

        <button
          type="submit"
          className="w-full py-2 bg-primary text-white font-semibold rounded-md hover:bg-blue-800 focus:outline-none"
        >
          Reset Password
        </button>
      </form>
    </div>
  );
};

export default ResetPasswordPage;
