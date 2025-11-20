import React, { useState } from 'react';
import { useAuthStatus } from '../../ViewModels/useAuthStatus';

const API_BASE_URL = 'http://localhost:8000';

export const ProfileForm = () => {
    const { getAuthHeaders } = useAuthStatus();
    const [nomePerfil, setNomePerfil] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    
    // Estado para permissões selecionadas (IDs fictícios mapeados para lógica do front)
    // No backend real, você precisaria buscar a lista de permissões disponíveis (`GET /permissoes`)
    // Aqui vou assumir IDs fixos se eles já existirem no seu banco seedado, 
    // ou você terá que criar as permissões antes.
    const [selectedPermissions, setSelectedPermissions] = useState([]);

    // Mapa de IDs de permissão (Exemplo: assumindo que no banco ID 1 = Logs, ID 2 = Alertas, etc)
    // Você deve ajustar isso conforme o que está no seu banco de dados (Tabela 'permissoes')
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
        setIsLoading(true);

        try {
            const payload = {
                nome: nomePerfil,
                permissoes_ids: selectedPermissions
            };

            const response = await fetch(`${API_BASE_URL}/perfis/`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Erro ao criar perfil');
            }

            alert('Perfil criado com sucesso!');
            setNomePerfil('');
            setSelectedPermissions([]);

        } catch (error) {
            alert(`Erro: ${error.message}`);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="p-8 bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg mx-auto">
            <h3 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
                HU-7: Criar Perfil de Permissão
            </h3>
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
                
                <div className="space-y-2 p-4 border rounded-md dark:border-gray-700">
                    <div className="flex items-center">
                        <input 
                            id="perm-logs" 
                            type="checkbox" 
                            className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                            checked={selectedPermissions.includes(PERMISSION_IDS.LOGS)}
                            onChange={() => handleCheckboxChange(PERMISSION_IDS.LOGS)}
                        />
                        <label htmlFor="perm-logs" className="ml-3 text-sm text-gray-700 dark:text-gray-300">Visualizar Logs em Tempo Real (HU-13)</label>
                    </div>
                    <div className="flex items-center">
                        <input 
                            id="perm-alerts" 
                            type="checkbox" 
                            className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                            checked={selectedPermissions.includes(PERMISSION_IDS.ALERTS)}
                            onChange={() => handleCheckboxChange(PERMISSION_IDS.ALERTS)}
                        />
                        <label htmlFor="perm-alerts" className="ml-3 text-sm text-gray-700 dark:text-gray-300">Visualizar Lista de Alertas</label>
                    </div>
                    <div className="flex items-center">
                        <input 
                            id="perm-users" 
                            type="checkbox" 
                            className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                            checked={selectedPermissions.includes(PERMISSION_IDS.USERS)}
                            onChange={() => handleCheckboxChange(PERMISSION_IDS.USERS)}
                        />
                        <label htmlFor="perm-users" className="ml-3 text-sm text-gray-700 dark:text-gray-300">Incluir/Editar Usuários (HU-1)</label>
                    </div>
                </div>

                <button 
                    type="submit" 
                    className="mt-6 w-full py-2 px-4 text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
                    disabled={isLoading}
                >
                    {isLoading ? 'Criando...' : 'Criar Perfil'}
                </button>
            </form>
        </div>
    );
}