import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStatus } from './ViewModels/useAuthStatus';

import { LoginScreen } from './Components/Auth/LoginScreen';
import { LogDashboardScreen } from './Components/Dashboard/LogDashboardScreen'; 
import { AlertsList } from './Components/Monitoring/AlertsList';
import { NewUserForm } from './Components/Users/NewUserForm';
import { ProfileForm } from './Components/Permissions/ProfileForm'; 
import { MainLayout } from './Components/Layout/MainLayout';

const ProtectedRoute = ({ isAuth, children }) => {
    if (!isAuth) {
        return <Navigate to="/login" replace />;
    }
    return children;
};

const PublicRoute = ({ isAuth, children }) => {
    if (isAuth) {
        return <Navigate to="/logs" replace />;
    }
    return children;
};

function App() {
  // Extraímos também o 'logout' aqui, pois o App é quem manda no estado
  const { login, logout, isAuthenticated } = useAuthStatus();

  return (
    <Router>
      <Routes>
        
        <Route 
          path="/login" 
          element={
            <PublicRoute isAuth={isAuthenticated}>
              <LoginScreen onLoginSuccess={login} />
            </PublicRoute>
          } 
        />

        <Route element={<ProtectedRoute isAuth={isAuthenticated}><MainLayout onLogout={logout} /></ProtectedRoute>}>
          {/* Note acima: Passamos onLogout={logout} para o MainLayout */}
          
          <Route index element={<Navigate to="/logs" replace />} />
          <Route path="/logs" element={<LogDashboardScreen />} />
          <Route path="/alerts" element={<AlertsList />} />
          <Route path="/users" element={
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <NewUserForm /> 
              <ProfileForm /> 
            </div>
          } />
        </Route>
        
        <Route path="*" element={<Navigate to="/logs" />} />
        
      </Routes>
    </Router>
  );
}

export default App;