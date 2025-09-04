import React, { useState } from 'react';
import PermissaoCheckbox from './PermissaoCheckbox'; // Componente pequeno para cada checkbox

function FormularioPerfil({ perfisExistentes, permissoesDisponiveis, onSave }) {
  const [nome, setNome] = useState('');
  const [permissoesSelecionadas, setPermissoesSelecionadas] = useState([]);
  const [erro, setErro] = useState('');
  const [sucesso, setSucesso] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setErro('');
    setSucesso('');

    // Validação de duplicidade (frontend)
    const nomeJaExiste = perfisExistentes.some(
      (perfil) => perfil.nome.toLowerCase() === nome.toLowerCase()
    );

    if (nomeJaExiste) {
      setErro('Já existe um perfil com este nome.');
      return;
    }

    if (nome.trim() === '') {
      setErro('O nome do perfil não pode ser vazio.');
      return;
    }

    if (permissoesSelecionadas.length === 0) {
      setErro('Selecione ao menos uma permissão.');
      return;
    }

    onSave({ nome, permissoes: permissoesSelecionadas });
    setSucesso(`Perfil '${nome}' criado com sucesso!`);
    setNome('');
    setPermissoesSelecionadas([]);
    // Em um cenário real, você resetaria os checkboxes.
    // Para simplificar, estamos apenas limpando o estado.
  };

  const handlePermissaoChange = (permissao, checked) => {
    if (checked) {
      setPermissoesSelecionadas((prev) => [...prev, permissao]);
    } else {
      setPermissoesSelecionadas((prev) => prev.filter((p) => p !== permissao));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="profileName" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Perfil Nome:</label>
        <input 
          type="text" 
          id="profileName"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-gray-50 dark:bg-gray-700 dark:text-gray-100"
          placeholder="e.g., Analista de Segurança"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Permissoes:</label>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {permissoesDisponiveis.map((permissao) => (
            <PermissaoCheckbox
              key={permissao}
              permissao={permissao}
              isChecked={permissoesSelecionadas.includes(permissao)}
              onChange={handlePermissaoChange}
            />
          ))}
        </div>
      </div>
      
      {erro && (
        <p className="text-red-500 text-sm">{erro}</p>
      )}
      {sucesso && (
        <p className="text-green-500 text-sm">{sucesso}</p>
      )}

      <button 
        type="submit"
        className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Perfil criado 
      </button>
    </form>
  );
}

export default FormularioPerfil;
