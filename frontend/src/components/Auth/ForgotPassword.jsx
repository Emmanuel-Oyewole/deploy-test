import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [errorMessage, setErrorMessage] = useState(""); // Error handling
  const [successMessage, setSuccessMessage] = useState(""); // Success message
  const navigate = useNavigate();

  const handleChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      

      const response = await axios.post(
        `http://localhost:8000/auth/forgot-password?email=${encodeURIComponent(email)}`,
        {},
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        setSuccessMessage("A password reset link has been sent to your email.");
        setEmail("");
        // navigate("/reset-password");
      } else {
        setErrorMessage("Something went wrong. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);

      // Check if the backend responded with an error
      if (error.response) {
        // Check for specific email not found error
        if (error.response.status === 404) {
          setErrorMessage("Incorrect Email Please check and try again.");
        } else {
          // Handle other errors returned by the backend
          setErrorMessage(
            error.response.data.message ||
              "An error occurred while sending the reset link."
          );
        }
      } else {
        // Handle network errors or unexpected errors
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
          Forgot Password
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
            Enter your email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-primary"
          />
        </div>

        <button
          type="submit"
          className="w-full py-2 bg-primary text-white font-semibold rounded-md hover:bg-blue-800 focus:outline-none"
        >
          Send Reset Link
        </button>
      </form>
    </div>
  );
};

export default ForgotPassword;
