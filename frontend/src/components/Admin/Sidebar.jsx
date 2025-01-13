const Sidebar = () => {
  return (
    <div className="w-64 bg-gray-800 text-white p-4">
      <ul>
        <li className="mb-4"><a href="#" className="hover:underline">Dashboard</a></li>
        <li className="mb-4"><a href="#" className="hover:underline">Settings</a></li>
        <li className="mb-4"><a href="#" className="hover:underline">Profile</a></li>
        <li className="mb-4"><a href="#" className="hover:underline">Logout</a></li>
      </ul>
    </div>
  );
};

export default Sidebar;