import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStatus } from './ViewModels/useAuthStatus';

// Importação das Telas
import { LoginScreen } from './Components/Auth/LoginScreen';
import { LogDashboardScreen } from './Components/Dashboard/LogDashboardScreen'; 
import { AlertsList } from './Components/Monitoring/AlertsList';

import { UsersPage } from './Components/Users/UsersPage'; 
import { MainLayout } from './Components/Layout/MainLayout';

// Componente para proteger rotas privadas; Se não estiver autenticado, redireciona para o login
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
  // O App é o "dono" da verdade sobre o estado de autenticação
  const { login, logout, isAuthenticated } = useAuthStatus();

  return (
    <Router>
      <Routes>
        
        {/* A rota raiz ("/") manda explicitamente para o Login --- */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Rota de Login: Só acessível se NÃO estiver logado */}
        <Route 
          path="/login" 
          element={
            <PublicRoute isAuth={isAuthenticated}>
              <LoginScreen onLoginSuccess={login} />
            </PublicRoute>
          } 
        />

        {/* Rotas Protegidas: Acessíveis apenas se estiver logado */}
        <Route element={
            <ProtectedRoute isAuth={isAuthenticated}>
                {/* Passamos a função de logout para o layout (botão Sair) */}
                <MainLayout onLogout={logout} />
            </ProtectedRoute>
        }>
          
          {/* Removemos a rota 'index' daqui, pois a raiz "/" já é tratada acima */}
          {/* <Route index element={<Navigate to="/logs" replace />} /> */}
          
          {/* Monitoramento (HU-13) */}
          <Route path="/logs" element={<LogDashboardScreen />} />
          
          {/* Alertas */}
          <Route path="/alerts" element={<AlertsList />} />
          
          {/* Gestão de Usuários (HU-1 e HU-7) - Agora centralizado na UsersPage */}
          <Route path="/users" element={<UsersPage />} />

        </Route>
        
        {/* Rota de Fallback (404) - Redireciona qualquer rota desconhecida */}
        <Route path="*" element={<Navigate to="/login" />} />

      </Routes>
    </Router>
  );
}

export default App;