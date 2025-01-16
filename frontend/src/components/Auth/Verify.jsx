import { useState } from "react";
import axios from "axios";

const VerifyPage = () => {
  const [formData, setFormData] = useState({
    verificationCode: "",
  });
  const [verificationSuccess, setVerificationSuccess] = useState(false); // Track success
  const [errorMessage, setErrorMessage] = useState(""); // Error handling

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
      // Send the verification code to the backend
      const response = await axios.post(
        "http://localhost:8000/auth/verify_email",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        // If verification is successful, show success prompt
        setVerificationSuccess(true);
        setFormData({ verificationCode: "" });
      } else {
        setErrorMessage("Verification failed. Please check the code.");
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("An error occurred during verification.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-primary">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-semibold text-primary mb-6">
          Enter Verification Code
        </h2>

        <div className="mb-4">
          <label htmlFor="verificationCode" className="block text-primary mb-2">
            Verification Code
          </label>
          <input
            type="text"
            id="verificationCode"
            name="verificationCode"
            value={formData.verificationCode}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-primary"
          />
        </div>

        <button
          type="submit"
          className="w-full py-2 bg-primary text-white font-semibold rounded-md hover:bg-blue-800 focus:outline-none"
        >
          Verify
        </button>
      </form>

      {verificationSuccess && (
        <div className="mt-6 p-4 bg-green-100 text-green-700 rounded-md shadow-md">
          <p className="text-center font-semibold">
            Your email has been successfully verified. Your account will be
            inactive until the admin approves your enrollment request.
          </p>
        </div>
      )}

      {errorMessage && (
        <div className="mt-6 p-4 bg-red-100 text-red-700 rounded-md shadow-md">
          <p className="text-center font-semibold">{errorMessage}</p>
        </div>
      )}
    </div>
  );
};

export default VerifyPage;
