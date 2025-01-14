import { Navigate } from 'react-router-dom';
import { jwtDecode } from "jwt-decode";
import PropTypes from 'prop-types';

const ProtectedRoute = ({ children, roles }) => {
  const token = document.cookie
    .split("; ")
    .find((row) => row.startsWith("token="))
    ?.split("=")[1];
  console.log("Fetched token:", token);

  if (!token) {
    console.log("Redirecting to login due to missing token");
    return <Navigate to="/home" />;
  }

  const user = jwtDecode(token);
  console.log("Decoded token:", user);

  if (!user || !roles.includes(user.role)) {
    console.log("Redirecting to login due to invalid role");
    return <Navigate to="/home" />;
  }

  return children;
};

export default ProtectedRoute;
