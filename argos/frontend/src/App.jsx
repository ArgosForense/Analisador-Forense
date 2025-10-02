import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStatus } from './ViewModels/useAuthStatus';

// Views
import { LoginScreen } from './Components/Auth/LoginScreen';
import { LogMonitorTable } from './Components/Monitoring/LogMonitorTable';
import { AlertsList } from './Components/Monitoring/AlertsList';
import { NewUserForm } from './Components/Users/NewUserForm';
import { ProfileForm } from './Components/Permissions/ProfileForm'; // HU-7
import { MainLayout } from './Components/Layout/MainLayout'; // Layout com o Menu Superior

// Componente para proteger rotas (garantir que o usuário esteja logado)
const ProtectedRoute = ({ children }) => {
    const { isAuthenticated } = useAuthStatus();
    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }
    return children;
};

function App() {
  const { login } = useAuthStatus();
  
  // Passa a função de login para a tela de login
  // (A tela de login deve chamar 'login()' em caso de sucesso)

  return (
    <Router>
      <Routes>
        
        {/* Rota de Login (Não Protegida) */}
        <Route path="/login" element={<LoginScreen onLoginSuccess={login} />} />

        {/* Rota Protegida (Dashboard e Telas Internas) */}
        <Route element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
          
          {/* Rota Inicial (Redireciona para Logs) */}
          <Route index element={<Navigate to="/logs" replace />} />
          
          {/* HU-13: Logs */}
          <Route path="/logs" element={<LogMonitorTable />} />
          
          {/* Lista de Alertas */}
          <Route path="/alerts" element={<AlertsList />} />
          
          {/* HU-1, HU-7, HU-8: Gestão de Usuários e Perfis */}
          <Route path="/users" element={
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <NewUserForm /> {/* HU-1 (Incluir Usuário) e HU-8 (Atribuir Perfil) */}
              <ProfileForm /> {/* HU-7 (Criar Perfil) */}
            </div>
          } />

        </Route>
        
        {/* Rota para qualquer URL não encontrada */}
        <Route path="*" element={<Navigate to="/logs" />} />
        
      </Routes>
    </Router>
  );
}

export default App;