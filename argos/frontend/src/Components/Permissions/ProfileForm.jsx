import React, { useState } from 'react';

export const ProfileForm = ({ profiles, onCreate, onDelete, isLoading, error }) => {
    
    const [nomePerfil, setNomePerfil] = useState('');
    const [selectedPermissions, setSelectedPermissions] = useState([]);

    const PERMISSION_IDS = {
        LOGS: 1,
        ALERTS: 2,
        USERS: 3
    };

    const handleCheckboxChange = (permId) => {
        setSelectedPermissions(prev => {
            if (prev.includes(permId)) {
                return prev.filter(id => id !== permId);
            } else {
                return [...prev, permId];
            }
        });
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
        <div className="space-y-8">
            {/* --- Formulário de Criação --- */}
            <div className="p-8 bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg mx-auto">
                <h3 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
                    Criar Perfil Com Permissão
                </h3>
                
                {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Nome do Perfil</label>
                        <input 
                            type="text" 
                            value={nomePerfil}
                            onChange={(e) => setNomePerfil(e.target.value)}
                            placeholder="Ex: Analista Nível 3" 
                            className="mt-1 block w-full rounded-md border p-2 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600" 
                            required 
                        />
                    </div>
                    
                    <h4 className="text-lg font-medium mb-3 text-gray-900 dark:text-white">
                        Configurar Permissões
                    </h4>
                    
                    <div className="space-y-2 p-4 border rounded-md dark:border-gray-700 mb-6">
                        <div className="flex items-center">
                            <input 
                                id="perm-logs" type="checkbox" className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                                checked={selectedPermissions.includes(PERMISSION_IDS.LOGS)}
                                onChange={() => handleCheckboxChange(PERMISSION_IDS.LOGS)}
                            />
                            <label htmlFor="perm-logs" className="ml-3 text-sm text-gray-700 dark:text-gray-300">Visualizar Logs em Tempo Real</label>
                        </div>
                        <div className="flex items-center">
                            <input 
                                id="perm-alerts" type="checkbox" className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                                checked={selectedPermissions.includes(PERMISSION_IDS.ALERTS)}
                                onChange={() => handleCheckboxChange(PERMISSION_IDS.ALERTS)}
                            />
                            <label htmlFor="perm-alerts" className="ml-3 text-sm text-gray-700 dark:text-gray-300">Visualizar Alertas</label>
                        </div>
                        <div className="flex items-center">
                            <input 
                                id="perm-users" type="checkbox" className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                                checked={selectedPermissions.includes(PERMISSION_IDS.USERS)}
                                onChange={() => handleCheckboxChange(PERMISSION_IDS.USERS)}
                            />
                            <label htmlFor="perm-users" className="ml-3 text-sm text-gray-700 dark:text-gray-300">Gerenciar Usuários </label>
                        </div>
                    </div>

                    <button 
                        type="submit" 
                        className="w-full py-2 px-4 text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
                        disabled={isLoading}
                    >
                        {isLoading ? 'Processando...' : 'Criar Perfil'}
                    </button>
                </form>
            </div>

            {/* --- Lista de Perfis Existentes (Com Botão de Delete) --- */}
            <div className="p-8 bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg mx-auto">
                <h4 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
                    Perfis Existentes
                </h4>
                <div className="space-y-2 max-h-60 overflow-y-auto">
                    {profiles.length > 0 ? (
                        profiles.map(profile => (
                            <div key={profile.id} className="flex justify-between items-center p-3 border rounded-md dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                                <span className="text-gray-800 dark:text-gray-200 font-medium">
                                    {profile.nome}
                                </span>
                                <button
                                    onClick={() => onDelete(profile.id)} // Chama função do pai
                                    className="text-red-600 hover:text-red-800 text-sm font-semibold px-2 py-1 rounded hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
                                    title="Excluir Perfil"
                                    disabled={isLoading}
                                >
                                    Excluir
                                </button>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-500 text-sm text-center">Nenhum perfil cadastrado.</p>
                    )}
                </div>
            </div>
        </div>
    );
}