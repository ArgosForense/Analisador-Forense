import React from 'react';
import { TrashIcon, NoSymbolIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

export const UserList = ({ users, profiles, onDelete, onToggleStatus }) => {

    // Lógica corrigida e simplificada
    const getProfileName = (user) => {
        // 1. Tenta ler direto do objeto (Graças ao ajuste no Schema do Backend)
        if (user.perfil && user.perfil.nome) {
            return user.perfil.nome;
        }

        // 2. Fallback: Se veio só o ID (perfil_id), procura na lista de props
        const idToSearch = user.perfil_id || user.perfil; 
        if (!idToSearch) return 'Sem Perfil';

        // Garante comparação segura entre String e ObjectId
        const found = profiles.find(p => 
            String(p.id) === String(idToSearch) || 
            String(p._id) === String(idToSearch)
        );
        
        return found ? found.nome : 'Perfil Desconhecido';
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Usuários Cadastrados
                </h3>
            </div>
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700 table-fixed">
                    <thead className="bg-gray-50 dark:bg-gray-700/50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/4">Nome</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/3">Email Institucional</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/6">Perfil</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-32">Status</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-32">Ações</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:divide-gray-700">
                        {users.length > 0 ? (
                            users.map((user) => (
                                <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white truncate">
                                        {user.nome}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400 truncate">
                                        {user.email}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300">
                                            {getProfileName(user)}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-center">
                                        <div className="flex justify-center w-20 mx-auto">
                                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                                user.status === 'ATIVO' 
                                                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' 
                                                : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'}`}>
                                                {user.status}
                                            </span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <div className="flex justify-end gap-3">
                                            <button 
                                                onClick={() => onToggleStatus(user)}
                                                className={`p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors ${
                                                    user.status === 'ATIVO' ? 'text-orange-500' : 'text-green-500'
                                                }`}
                                                title={user.status === 'ATIVO' ? "Desativar" : "Ativar"}
                                            >
                                                {user.status === 'ATIVO' ? <NoSymbolIcon className="h-5 w-5" /> : <CheckCircleIcon className="h-5 w-5" />}
                                            </button>
                                            <button 
                                                onClick={() => onDelete(user.id)}
                                                className="text-red-600 hover:text-red-900 p-1 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                                                title="Excluir Usuário"
                                            >
                                                <TrashIcon className="h-5 w-5" />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="5" className="px-6 py-10 text-center text-sm text-gray-500 dark:text-gray-400">
                                    Nenhum usuário encontrado.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};