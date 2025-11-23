import React from 'react';
import { NewUserForm } from './NewUserForm';
import { ProfileForm } from '../Permissions/ProfileForm';
import { useProfileViewModel } from '../../ViewModels/useProfileViewModel';

export const UsersPage = () => {
    // Usamos o ViewModel aqui para buscar os dados
    const { profiles, createProfile, deleteProfile, isLoading, error } = useProfileViewModel();

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Passamos a lista de perfis atualizada para o NewUserForm */}
            <NewUserForm profiles={profiles} isLoading={isLoading} />
            
            {/* Passamos as funções e dados para o ProfileForm */}
            <ProfileForm 
                profiles={profiles} 
                onCreate={createProfile} 
                onDelete={deleteProfile} 
                isLoading={isLoading} 
                error={error}
            />
        </div>
    );
};