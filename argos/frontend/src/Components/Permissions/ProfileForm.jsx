import React, { useState } from 'react';
import { TrashIcon, PlusIcon } from '@heroicons/react/24/outline'; // Ícones

export const ProfileForm = ({ profiles, onCreate, onDelete, isLoading, error }) => {
    const [nomePerfil, setNomePerfil] = useState('');
    const [selectedPermissions, setSelectedPermissions] = useState([]);

    const PERMISSION_IDS = { LOGS: 1, ALERTS: 2, USERS: 3 };

    const handleCheckboxChange = (permId) => {
        setSelectedPermissions(prev => 
            prev.includes(permId) ? prev.filter(id => id !== permId) : [...prev, permId]
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const success = await onCreate(nomePerfil, selectedPermissions);
        if (success) {
            alert('Perfil criado com sucesso!');
            setNomePerfil('');
            setSelectedPermissions([]);
        }
    };

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Coluna Esquerda: Formulário */}
            <div className="space-y-5">
                {error && (
                    <div className="bg-red-50 text-red-700 p-3 rounded-lg text-sm border border-red-200">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="flex flex-col h-full justify-between">
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Nome do Novo Perfil</label>
                            <input 
                                type="text" 
                                value={nomePerfil}
                                onChange={(e) => setNomePerfil(e.target.value)}
                                placeholder="Ex: Auditor Externo" 
                                className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 px-3 dark:bg-gray-700 dark:border-gray-600 dark:text-white" 
                                required 
                            />
                        </div>
                        
                        <div>
                            <span className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Permissões</span>
                            <div className="bg-gray-50 dark:bg-gray-900/50 p-3 rounded-lg border border-gray-200 dark:border-gray-600 space-y-2">
                                <label className="flex items-center space-x-3 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 p-1 rounded transition">
                                    <input 
                                        type="checkbox" 
                                        className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                                        checked={selectedPermissions.includes(PERMISSION_IDS.LOGS)}
                                        onChange={() => handleCheckboxChange(PERMISSION_IDS.LOGS)}
                                    />
                                    <span className="text-sm text-gray-700 dark:text-gray-300">Visualizar Logs</span>
                                </label>
                                <label className="flex items-center space-x-3 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 p-1 rounded transition">
                                    <input 
                                        type="checkbox" 
                                        className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                                        checked={selectedPermissions.includes(PERMISSION_IDS.ALERTS)}
                                        onChange={() => handleCheckboxChange(PERMISSION_IDS.ALERTS)}
                                    />
                                    <span className="text-sm text-gray-700 dark:text-gray-300">Visualizar Alertas</span>
                                </label>
                                <label className="flex items-center space-x-3 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 p-1 rounded transition">
                                    <input 
                                        type="checkbox" 
                                        className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                                        checked={selectedPermissions.includes(PERMISSION_IDS.USERS)}
                                        onChange={() => handleCheckboxChange(PERMISSION_IDS.USERS)}
                                    />
                                    <span className="text-sm text-gray-700 dark:text-gray-300">Gerenciar Usuários</span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <button 
                        type="submit" 
                        className="mt-6 w-full inline-flex items-center justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-all"
                        disabled={isLoading}
                    >
                        <PlusIcon className="h-5 w-5 mr-2" />
                        {isLoading ? 'Criando...' : 'Criar Perfil'}
                    </button>
                </form>
            </div>

            {/* Coluna Direita: Lista de Perfis */}
            <div className="flex flex-col h-full">
                <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3 uppercase tracking-wide">
                    Perfis Existentes ({profiles.length})
                </h4>
                
                <div 
                    className="flex-1 overflow-y-auto pr-1 space-y-2 max-h-[300px]"
                    style={{ scrollbarWidth: 'thin', scrollbarColor: '#CBD5E1 transparent' }} // Estilo sutil para Firefox
                >
                    {/* CSS para scrollbar Webkit (Chrome/Safari) */}
                    <style>{`
                        ::-webkit-scrollbar { width: 6px; }
                        ::-webkit-scrollbar-track { background: transparent; }
                        ::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 20px; }
                        .dark ::-webkit-scrollbar-thumb { background-color: #4b5563; }
                    `}</style>

                    {profiles.length > 0 ? (
                        profiles.map(profile => (
                            <div key={profile.id} className="group flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-indigo-300 dark:hover:border-indigo-500 transition-colors">
                                <div className="flex items-center">
                                    <div className="h-2 w-2 rounded-full bg-indigo-500 mr-3"></div>
                                    <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                                        {profile.nome}
                                    </span>
                                </div>
                                <button
                                    onClick={() => onDelete(profile.id)}
                                    className="text-gray-400 hover:text-red-600 p-1.5 rounded-full hover:bg-red-50 dark:hover:bg-red-900/30 transition-all"
                                    title="Excluir Perfil"
                                    disabled={isLoading}
                                >
                                    <TrashIcon className="h-5 w-5" />
                                </button>
                            </div>
                        ))
                    ) : (
                        <div className="flex flex-col items-center justify-center h-32 text-gray-400 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-lg">
                            <p className="text-sm">Nenhum perfil encontrado.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}