import React from 'react';
import FormularioPerfil from '../components/FormularioPerfil';
import ListaPerfis from '../components/ListaPerfis';

function GerenciadorPerfisView({ perfis, permissoesDisponiveis, onAdicionarPerfil, onDeletarPerfil }) {
  return (
    <div className="space-y-6">
      {/* Seção de Criação de Perfil */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">Criar Novo Usuario</h2>
        <FormularioPerfil 
          perfisExistentes={perfis}
          permissoesDisponiveis={permissoesDisponiveis}
          onSave={onAdicionarPerfil}
        />
      </div>

      {/* Seção de Perfis Existentes */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">Perfis de Usuarios Existentes</h2>
        <ListaPerfis 
          perfis={perfis} 
          onDeletarPerfil={onDeletarPerfil}
        />
      </div>
    </div>
  );
}

export default GerenciadorPerfisView;
