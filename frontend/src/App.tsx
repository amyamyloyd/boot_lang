import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import POCBuilder from './components/POCBuilder';
import Login from './components/Login';
import Register from './components/Register';
import UserSettings from './components/UserSettings';
import AdminPanel from './components/AdminPanel';

// Protected route wrapper
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

// Navigation component
const Navigation: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex space-x-4">
            <Link to="/" className="text-xl font-bold hover:text-blue-200">
              Boot_Lang
            </Link>
            {isAuthenticated && (
              <>
                <Link to="/" className="px-3 py-2 rounded hover:bg-blue-700">
                  POC Builder
                </Link>
                <Link to="/settings" className="px-3 py-2 rounded hover:bg-blue-700">
                  Settings
                </Link>
                {user?.is_admin && (
                  <Link to="/admin" className="px-3 py-2 rounded hover:bg-blue-700">
                    Admin Panel
                  </Link>
                )}
              </>
            )}
          </div>
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-sm">Welcome, {user?.username}</span>
                <button
                  onClick={logout}
                  className="px-4 py-2 bg-blue-700 rounded hover:bg-blue-800"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="px-4 py-2 bg-blue-700 rounded hover:bg-blue-800">
                  Login
                </Link>
                <Link to="/register" className="px-4 py-2 bg-blue-700 rounded hover:bg-blue-800">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

// Main App component
const AppContent: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <div className="max-w-7xl mx-auto">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <POCBuilder />
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <UserSettings />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <ProtectedRoute>
                <AdminPanel />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;