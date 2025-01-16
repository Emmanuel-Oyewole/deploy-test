import  { useState } from 'react';
import axios from 'axios';
import Sidebar from '../../components/Admin/Sidebar';
import UserList from '../../components/Admin/UserList';


const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/get_users');
      setUsers(response.data);
    } catch (err) {
      setError('Failed to fetch users');
    }
  };

  const handleUserAction = async (email, action) => {
    try {
      const endpoint = `/api/users/${action}`;
      await axios.post(endpoint, { email });
      fetchUsers(); // Refresh the user list after the action
    } catch (err) {
      setError(`Failed to ${action} user`);
    }
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1 p-8">
        <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
        <button
          onClick={fetchUsers}
          className="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
        >
          Display All Users
        </button>
        {error && <p className="text-red-500">{error}</p>}
        <UserList users={users} onUserAction={handleUserAction} />
      </div>
    </div>
  );
};

export default AdminDashboard;
