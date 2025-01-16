import { useState } from "react";

const Sidebar = ({ profilePicture, name, menuItems, onMenuItemClick, onLogout }) => {
  const [isOpen, setIsOpen] = useState(true); // Controls sidebar open/close

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <aside
      className={`transition-all duration-300 bg-[#071B63] text-white flex flex-col items-center py-6 ${
        isOpen ? "w-64" : "w-20"
      }`}
    >
      {/* Sidebar Toggle Button */}
      <button
        onClick={handleToggle}
        className="absolute top-4 left-4 text-white bg-[#071B63] rounded-full p-2 hover:bg-[#0b255a] focus:outline-none"
      >
        {isOpen ? "◁" : "▷"}
      </button>

      {/* Profile Picture */}
      <div className="w-16 h-16 rounded-full bg-white mb-4 overflow-hidden">
        {profilePicture ? (
          <img
            src={profilePicture}
            alt="Profile"
            className="w-full h-full rounded-full object-cover"
          />
        ) : null}
      </div>

      {/* Menu Items */}
      <div className="flex flex-col items-center mt-4">
        {menuItems.map((item, index) => (
          <button
            key={index}
            onClick={() => onMenuItemClick(item.title)}
            className="w-full px-4 py-2 my-2 text-left hover:bg-[#0b255a] focus:outline-none"
          >
            {item.title}
          </button>
        ))}
      </div>

      {/* Logout Button */}
      <button
        onClick={onLogout}
        className="mt-auto mb-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 focus:outline-none"
      >
        Logout
      </button>
    </aside>
  );
};

export default Sidebar;