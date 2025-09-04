import React from 'react';

function PermissaoCheckbox({ permissao, isChecked, onChange }) {
  const formattedPermissao = permissao
    .replace(/_/g, ' ') // Substitui underscores por espaços
    .replace(/\b\w/g, (char) => char.toUpperCase()); // Capitaliza a primeira letra de cada palavra

  return (
    <div className="flex items-center">
      <input
        id={permissao}
        name="permissoes"
        type="checkbox"
        checked={isChecked}
        onChange={(e) => onChange(permissao, e.target.checked)}
        className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
      />
      <label htmlFor={permissao} className="ml-2 block text-sm text-gray-900 dark:text-gray-100">
        {formattedPermissao}
      </label>
    </div>
  );
}

export default PermissaoCheckbox;
