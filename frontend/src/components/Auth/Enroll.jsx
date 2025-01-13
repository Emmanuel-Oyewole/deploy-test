import { useState } from "react";
import axios from "axios";

const Enroll = () => {
  const [formData, setFormData] = useState({
    fullname: "",
    email: "",
    user_type: "Student",
  });

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
      // Make a POST request using Axios
      const response = await axios.post(
        "http://localhost:8000/auth/enroll",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      // Check if the response is successful
      if (response.status === 201) {
        alert("You account enrollment is under consideration, await admins approval");
        setFormData({ fullname: "", email: "", user_type: "Student" });
      } else {
        alert("Enrollment failed.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert(error.response.data.detail);
      setFormData({ fullname: "", email: "", user_type: "Student" });
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-primary">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-semibold text-primary mb-6 text-center">
          Enroll
        </h2>
        <div className="mb-4">
          <label htmlFor="fullname" className="block text-primary mb-2">
            Fullname
          </label>
          <input
            type="text"
            id="fullname"
            name="fullname"
            value={formData.fullname}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-primary"
          />
        </div>
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
        <div className="mb-6">
          <label htmlFor="user_type" className="block text-primary mb-2">
            User Type
          </label>
          <select
            id="user_type"
            name="user_type"
            value={formData.user_type}
            onChange={handleChange}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-primary"
          >
            <option value="Admin">Admin</option>
            <option value="Student">Student</option>
            <option value="Teacher">Teacher</option>
            <option value="Parent">Parent</option>
          </select>
        </div>
        <button
          type="submit"
          className="w-full py-2 bg-primary text-white font-semibold rounded-md hover:bg-blue-800 focus:outline-none"
        >
          Enroll
        </button>
      </form>
    </div>
  );
};

export default Enroll;
