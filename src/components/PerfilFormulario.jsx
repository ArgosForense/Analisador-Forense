import React, { useState } from "react";
import PermissionCheckbox from "../components/PermissaoCheckbox";

const PERMISSIONS = ["Ler", "Escrever", "Editar", "Deletar"];

export default function ProfileForm({ onAddProfile }) {
  const [nome, setNome] = useState("");
  const [permissions, setPermissions] = useState([]);

  const handleCheckboxChange = (perm) => {
    if (permissions.includes(perm)) {
      setPermissions(permissions.filter((p) => p !== perm));
    } else {
      setPermissions([...permissions, perm]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!nome) return alert("Digite um nome para o perfil.");
    onAddProfile({ nome, permissions });
    setNome("");
    setPermissions([]);
  };

  return (
    <form
      onSubmit={handleSubmit}
      classNome="p-4 bg-white shadow rounded-lg space-y-4"
    >
      <input
        type="text"
        placeholder="Nome do perfil"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
        classNome="w-full p-2 border rounded"
      />

      <div classNome="grid grid-cols-2 gap-2">
        {PERMISSIONS.map((perm) => (
          <PermissionCheckbox
            key={perm}
            label={perm}
            checked={permissions.includes(perm)}
            onChange={() => handleCheckboxChange(perm)}
          />
        ))}
      </div>

      <button
        type="submit"
        classNome="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Criar Perfil
      </button>
    </form>
  );
}

