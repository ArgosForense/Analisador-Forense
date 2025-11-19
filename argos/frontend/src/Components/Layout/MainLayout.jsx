import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Header } from './Header';

export const MainLayout = () => {
    const navigate = useNavigate();
    
    const user = { name: 'Matheus Vinycius', profile: 'Gestor de SOC' };

    const handleLogout = () => {
        console.log("Usuário deslogado.");
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
            <Header 
                userProfile={user.profile} 
                handleLogout={handleLogout} 
            />
            
            {/* Conteúdo específico da rota será renderizado aqui */}
            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <Outlet />
            </main>
        </div>
    );
};