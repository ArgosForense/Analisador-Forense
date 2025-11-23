import React from 'react';

export const NewUserForm = ({ profiles, formData, handleChange, handleSubmit, isLoading }) => {
  // Removemos o hook interno. Tudo vem via props.
  const inputClass = "mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2.5 px-3 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-all duration-200";

  return (
      <form onSubmit={(e) => { e.preventDefault(); handleSubmit(); }} className="space-y-5">
        {/* Nome */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Nome Completo</label>
          <input type="text" name="name" required className={inputClass} value={formData.name} onChange={handleChange} disabled={isLoading} />
        </div>
        {/* E-mail */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">E-mail Pessoal</label>
          <input type="email" name="email" required className={inputClass} value={formData.email} onChange={handleChange} disabled={isLoading} />
        </div>
        {/* Perfil */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Perfil de Acesso</label>
          <select name="profileId" required className={inputClass} value={formData.profileId} onChange={handleChange} disabled={isLoading}>
            <option value="">Selecione um perfil...</option>
            {profiles.map((p) => <option key={p.id} value={p.id}>{p.nome}</option>)}
          </select>
        </div>
        <div className="pt-2">
            <button type="submit" disabled={isLoading} className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 transition-all">
            {isLoading ? 'Processando...' : 'Incluir Usuário'}
            </button>
        </div>
      </form>
  );
};