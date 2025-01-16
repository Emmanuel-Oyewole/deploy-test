import Sidebar from "../../components/Student/Sidebar";
import MainContent from "../../components/Student/MainContent";
import { useState } from "react";
import axiosInstance from "../../services/axiosLogin";
import { useNavigate } from "react-router-dom";

const StudentDashboard = () => {
  const [selectedTitle, setSelectedTitle] = useState(
    "Welcome to Student Dashboard"
  );
  const navigate = useNavigate();

  const menuItems = [
    { title: "Assignment Page" },
    { title: "Material Page" },
    { title: "Results Page" },
    { title: "Information Page" },
  ];

  const handleMenuItemClick = (title) => {
    setSelectedTitle(title);
  };
  const handleLogout = async () => {
    try {
      await axiosInstance.post("/auth/logout");
      console.log("User logged out");
      navigate("/login");
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  return (
    <div className="flex h-screen bg-[#f8f9fc]">
      {/* Sidebar Component */}
      <Sidebar
        profilePicture={null} // Replace `null` with a URL for a real profile picture
        name="John Doe"
        menuItems={menuItems}
        onMenuItemClick={handleMenuItemClick}
        onLogout={handleLogout}
      />

      {/* Main Content Component */}
      <MainContent selectedTitle={selectedTitle} />
    </div>
  );
};

export default StudentDashboard;
