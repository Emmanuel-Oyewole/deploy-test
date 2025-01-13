import PropTypes from 'prop-types';

const UserActions = ({ email, onUserAction }) => {
  return (
    <div className="flex space-x-2">
      <button
        onClick={() => onUserAction(email, 'activate')}
        className="px-2 py-1 bg-green-500 text-white rounded hover:bg-green-700"
      >
        Activate
      </button>
      <button
        onClick={() => onUserAction(email, 'deactivate')}
        className="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-700"
      >
        Deactivate
      </button>
      <button
        onClick={() => onUserAction(email, 'delete')}
        className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-700"
      >
        Delete
      </button>
    </div>
  );
};

UserActions.propTypes = {
  email: PropTypes.string.isRequired,
  onUserAction: PropTypes.func.isRequired,
};

export default UserActions;