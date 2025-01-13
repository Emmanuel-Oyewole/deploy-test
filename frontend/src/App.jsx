import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import EnrollPage from "./pages/Auth/EnrollPage";
import LogInPage from "./pages/Auth/LogInPage";
import ResetPage from "./pages/Auth/ResetPage";
import HomePage from "./pages/Home/HomePage";
import ForgotPasswordPage from "./pages/Auth/ForgotPasswordPage";
import StudentDashboard from "./pages/Student/StudentDashBoard";
import TeacherDashboard from "./pages/Teacher/TeacherDashBoard";
import AdminDashboard from "./pages/Admin/AdminDashBoard";
import ParentDashboard from "./pages/Parent/ParentDashBoard";
import ProtectedRoute from "./components/Auth/ProtectedRoute";
import NotFound from "./components/NotFound";

const App = () => {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/home" element={<HomePage />} />
        <Route path="/login" element={<LogInPage />} />
        <Route path="/enrol" element={<EnrollPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPage />} />
        <Route path="/notfound" element={<NotFound />} />

        {/* Protected Routes */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute roles={["Admin"]}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/teacher"
          element={
            <ProtectedRoute roles={["Teacher"]}>
              <TeacherDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/studentdashboard"
          element={
            <ProtectedRoute roles={["Student"]}>
              <StudentDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/parent"
          element={
            <ProtectedRoute roles={["Parent"]}>
              <ParentDashboard />
            </ProtectedRoute>
          }
        />

        {/* Redirect "/" to "/login" */}
        <Route path="/" element={<Navigate to="/home" replace />} />

        {/* Catch-all route for undefined paths */}
        <Route path="*" element={<Navigate to="/notfound" replace />} />
      </Routes>
    </Router>
  );
};

export default App;
