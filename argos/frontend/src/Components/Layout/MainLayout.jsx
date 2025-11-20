import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Header } from './Header';
// Removemos a importação do useAuthStatus daqui para evitar estado duplicado

// Recebemos onLogout via props do App.jsx
export const MainLayout = ({ onLogout }) => {
    const navigate = useNavigate();
    
    const user = { name: 'Matheus Vinycius', profile: 'Gestor de SOC' };

    const handleLogout = () => {
        // Chama a função do Pai (App.jsx)
        // Isso vai limpar o token E atualizar o estado 'isAuthenticated' globalmente
        onLogout(); 
        
        console.log("Usuário deslogado.");
        
        // Como o estado global mudou para false, o App.jsx vai renderizar 
        // as rotas públicas novamente, permitindo o acesso ao /login
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
            <Header 
                userProfile={user.profile} 
                handleLogout={handleLogout} 
            />
            
            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <Outlet />
            </main>
        </div>
    );
};