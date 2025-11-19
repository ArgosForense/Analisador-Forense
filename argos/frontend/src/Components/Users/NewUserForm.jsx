import React from 'react';
import { useNewUserViewModel } from '../../ViewModels/useNewUserViewModel';

export const NewUserForm = () => {
  const {
    formData,
    errors,
    profiles,
    isLoading,
    handleChange,
    handleSubmit,
  } = useNewUserViewModel();

  return (
    <div className="p-8 bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg mx-auto">
      <h3 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
        HU-1: Incluir Novo Usuário
      </h3>
      <form onSubmit={handleSubmit} className="space-y-6">
        
        {errors.general && (
            <p className="text-red-500 text-sm">{errors.general}</p>
        )}

        {/* Campo Nome */}
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Nome Completo
          </label>
          <input
            type="text"
            name="name"
            id="name"
            required
            className={`mt-1 block w-full rounded-md border p-2 dark:bg-gray-700 dark:text-white ${
                errors.name ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
            }`}
            value={formData.name}
            onChange={handleChange}
            disabled={isLoading}
          />
          {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name}</p>}
        </div>

        {/* Campo E-mail */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            E-mail
          </label>
          <input
            type="email"
            name="email"
            id="email"
            required
            className={`mt-1 block w-full rounded-md border p-2 dark:bg-gray-700 dark:text-white ${
                errors.email ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
            }`}
            value={formData.email}
            onChange={handleChange}
            disabled={isLoading}
          />
          {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email}</p>}
        </div>

        {/* Campo Perfil (HU-8) */}
        <div>
          <label htmlFor="profileId" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Perfil de Acesso (HU-8)
          </label>
          <select
            name="profileId"
            id="profileId"
            required
            className={`mt-1 block w-full rounded-md border p-2 dark:bg-gray-700 dark:text-white ${
                errors.profileId ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
            }`}
            value={formData.profileId}
            onChange={handleChange}
            disabled={isLoading}
          >
            <option value="">Selecione um perfil...</option>
            {profiles.map((profile) => (
              <option key={profile.id} value={profile.id}>
                {profile.name}
              </option>
            ))}
          </select>
          {errors.profileId && <p className="text-red-500 text-xs mt-1">{errors.profileId}</p>}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
        >
          {isLoading ? 'Incluindo...' : 'Incluir Usuário'}
        </button>
      </form>
    </div>
  );
};