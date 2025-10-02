import React from 'react';
// import { useProfileViewModel } from '../../ViewModels/useProfileViewModel'; 
// O ViewModel para HU-7 deve ser criado, seguindo a estrutura de useNewUserViewModel

export const ProfileForm = () => {
    // Apenas a View (UI) para HU-7: Criar Perfil de Permissão

    return (
        <div className="p-8 bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg mx-auto">
            <h3 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
                HU-7: Criar Perfil de Permissão
            </h3>
            <form>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Nome do Perfil</label>
                    <input type="text" placeholder="Ex: Analista Nível 3" className="mt-1 block w-full rounded-md border p-2 dark:bg-gray-700 dark:text-white border-gray-300 dark:border-gray-600" required />
                </div>
                
                <h4 className="text-lg font-medium mb-3 text-gray-900 dark:text-white">
                    Configurar Permissões
                </h4>
                
                <div className="space-y-2 p-4 border rounded-md dark:border-gray-700">
                    <div className="flex items-center">
                        <input id="perm-logs" type="checkbox" className="h-4 w-4 text-indigo-600 border-gray-300 rounded" />
                        <label htmlFor="perm-logs" className="ml-3 text-sm text-gray-700 dark:text-gray-300">Visualizar Logs em Tempo Real (HU-13)</label>
                    </div>
                    <div className="flex items-center">
                        <input id="perm-alerts" type="checkbox" className="h-4 w-4 text-indigo-600 border-gray-300 rounded" />
                        <label htmlFor="perm-alerts" className="ml-3 text-sm text-gray-700 dark:text-gray-300">Visualizar Lista de Alertas</label>
                    </div>
                    <div className="flex items-center">
                        <input id="perm-users" type="checkbox" className="h-4 w-4 text-indigo-600 border-gray-300 rounded" />
                        <label htmlFor="perm-users" className="ml-3 text-sm text-gray-700 dark:text-gray-300">Incluir/Editar Usuários (HU-1)</label>
                    </div>
                </div>

                <button type="submit" className="mt-6 w-full py-2 px-4 text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50">
                    Criar Perfil
                </button>
            </form>
        </div>
    );
}