import React from 'react';
import { NewUserForm } from './NewUserForm';
import { UserList } from './UserList'; 
import { ProfileForm } from '../Permissions/ProfileForm';
import { useProfileViewModel } from '../../ViewModels/useProfileViewModel';
import { useUserViewModel } from '../../ViewModels/useUserViewModel'; 
import { UserGroupIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';

export const UsersPage = () => {
    // Extraímos profiles e permissions do hook de perfil
    const { profiles, permissions, createProfile, deleteProfile, isLoading: loadingProfiles, error: errorProfiles } = useProfileViewModel();
    
    const { users, formData, handleChange, createUser, deleteUser, toggleStatus, isLoading: loadingUsers } = useUserViewModel();

    return (
        <div className="space-y-8 pb-10">
            <div className="border-b border-gray-200 pb-5 dark:border-gray-700">
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Gestão de Acesso</h2>
                <p className="mt-2 text-lg text-gray-500 dark:text-gray-400">Gerencie usuários, status e perfis.</p>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 items-start">
                {/* Novo Usuário */}
                <div className="xl:col-span-5">
                    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
                        <div className="p-6 border-b border-gray-100 dark:border-gray-700 flex items-center gap-3">
                            <div className="p-2 bg-indigo-50 dark:bg-indigo-900/30 rounded-lg text-indigo-600 dark:text-indigo-400">
                                <UserGroupIcon className="h-6 w-6" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Novo Usuário</h3>
                        </div>
                        <div className="p-6">
                            <NewUserForm 
                                profiles={profiles} 
                                formData={formData}
                                handleChange={handleChange}
                                handleSubmit={createUser}
                                isLoading={loadingUsers}
                            />
                        </div>
                    </div>
                </div>
                
                {/* Perfis */}
                <div className="xl:col-span-7">
                     <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden h-full">
                        <div className="p-6 border-b border-gray-100 dark:border-gray-700 flex items-center gap-3">
                            <div className="p-2 bg-indigo-50 dark:bg-indigo-900/30 rounded-lg text-indigo-600 dark:text-indigo-400">
                                <ShieldCheckIcon className="h-6 w-6" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Perfis de Permissão</h3>
                        </div>
                        <div className="p-6">
                            <ProfileForm 
                                profiles={profiles} 
                                permissions={permissions}
                                onCreate={createProfile} 
                                onDelete={deleteProfile} 
                                isLoading={loadingProfiles} 
                                error={errorProfiles}
                            />
                        </div>
                    </div>
                </div>
            </div>

            <div className="mt-8">
                 
                <UserList 
                    users={users} 
                    profiles={profiles}
                    onDelete={deleteUser} 
                    onToggleStatus={toggleStatus} 
                />
            </div>
        </div>
    );
};