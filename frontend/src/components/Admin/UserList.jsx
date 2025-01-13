import PropTypes from 'prop-types';
import UserActions from './UserAction';

const UserList = ({ users, onUserAction }) => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">All Users</h2>
      <div className="space-y-4">
        {users.map((user) => (
          <div key={user.id} className="flex justify-between items-center p-4 bg-white shadow rounded-md">
            <div>
              <p className="font-semibold">{user.name}</p>
              <p className="text-gray-600">{user.email}</p>
            </div>
            <UserActions email={user.email} onUserAction={onUserAction} />
          </div>
        ))}
      </div>
    </div>
  );
};

UserList.propTypes = {
  users: PropTypes.arrayOf(PropTypes.object).isRequired,
  onUserAction: PropTypes.func.isRequired,
};

export default UserList;