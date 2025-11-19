import React from 'react';
import { Link } from 'react-router-dom';

export const Header = ({ userProfile, handleLogout }) => {
  return (
    <nav className="bg-gray-800 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          
          {/* Logo e Nome do Sistema */}
          <div className="flex-shrink-0 flex items-center">
            <span className="text-xl font-bold text-indigo-400">Argos</span>
          </div>

          {/* Links de Navegação */}
          <div className="flex items-center space-x-4">
            <Link to="/logs" className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
              Monitoramento (HU-13)
            </Link>
            <Link to="/alerts" className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
              Alertas
            </Link>
            <Link to="/users" className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
              Gestão de Usuários (HU-1/HU-8)
            </Link>
          </div>

          {/* Área do Usuário / Logout */}
          <div className="flex items-center">
            <span className="text-sm font-medium text-gray-300 mr-4">
              {userProfile || 'Gestor SOC'}
            </span>
            <button
              onClick={handleLogout}
              className="px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
            >
              Sair
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};