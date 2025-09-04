import React from 'react';
import { PencilSquareIcon, TrashIcon } from '@heroicons/react/24/outline';

function ListaPerfis({ perfis, onDeletarPerfil }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead className="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              ID
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              Nome do Perfil
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              Permissões
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              Ações
            </th>
          </tr>
        </thead>
        <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          {perfis.map((perfil) => (
            <tr key={perfil.id}>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100">
                {perfil.id}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {perfil.nome}
              </td>
              <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-300">
                {perfil.permissoes.map(p => p.replace(/_/g, ' ')).join(', ')}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button 
                  onClick={() => console.log(`Editar perfil ${perfil.id}`)} // Lógica de edição real aqui
                  className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-600 mr-3"
                  title="Editar"
                >
                  <PencilSquareIcon className="w-5 h-5 inline-block" />
                </button>
                <button 
                  onClick={() => onDeletarPerfil(perfil.id)}
                  className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-600"
                  title="Deletar"
                >
                  <TrashIcon className="w-5 h-5 inline-block" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ListaPerfis;
