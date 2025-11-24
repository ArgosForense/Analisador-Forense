import { useState, useEffect, useCallback } from 'react';
import { useAuthStatus } from './useAuthStatus';

const API_BASE_URL = 'http://localhost:8000';

export const useUserViewModel = () => {
  const { getAuthHeaders } = useAuthStatus();
  
  const [users, setUsers] = useState([]);
  const [formData, setFormData] = useState({ name: '', email: '', profileId: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // --- LISTAR USUÁRIOS ---
  const fetchUsers = useCallback(async () => {
    setIsLoading(true);
    try {
        const headers = getAuthHeaders(); 
        const response = await fetch(`${API_BASE_URL}/usuarios/`, { headers: headers });
        
        if (response.ok) {
            const data = await response.json();
            // Garante que o ID seja lido corretamente, seja id ou _id
            const formattedData = data.map(u => ({
                ...u,
                id: u.id || u._id
            }));
            setUsers(formattedData);
        }
    } catch (err) {
        console.error(err);
        setError("Erro ao carregar usuários.");
    } finally {
        setIsLoading(false);
    }
  }, []); // Dependência vazia para evitar loop

  // --- CRIAR USUÁRIO ---
  const createUser = async () => {
    if (!formData.name || !formData.email || !formData.profileId) {
        alert("Preencha todos os campos.");
        return false;
    }
    setIsLoading(true);
    try {
        // CORREÇÃO AQUI: Removemos o parseInt(). O Mongo espera String.
        const payload = { 
            nome: formData.name, 
            email: formData.email, 
            perfil_id: formData.profileId // Envia como string direta
        };

        const response = await fetch(`${API_BASE_URL}/usuarios/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Erro ao criar usuário.");
        }
        
        alert(`Usuário ${formData.name} criado com sucesso!`);
        setFormData({ name: '', email: '', profileId: '' });
        await fetchUsers();
        return true;
    } catch (err) {
        alert(err.message);
        return false;
    } finally {
        setIsLoading(false);
    }
  };

  // --- DELETAR USUÁRIO ---
  const deleteUser = async (id) => {
      if (!window.confirm("Tem certeza que deseja excluir este usuário?")) return;
      setIsLoading(true);
      try {
          const response = await fetch(`${API_BASE_URL}/usuarios/${id}`, {
              method: 'DELETE',
              headers: getAuthHeaders()
          });
          if (!response.ok) throw new Error("Falha ao excluir.");
          
          setUsers(prev => prev.filter(u => u.id !== id));
      } catch (err) {
          alert(err.message);
      } finally {
          setIsLoading(false);
      }
  };

  // --- ALTERAR STATUS ---
  const toggleStatus = async (user) => {
      const action = user.status === 'ATIVO' ? 'desativar' : 'ativar';
      setIsLoading(true);
      try {
          const response = await fetch(`${API_BASE_URL}/usuarios/${user.id}/${action}`, {
              method: 'POST',
              headers: getAuthHeaders()
          });
          if (response.ok) {
              await fetchUsers();
          }
      } catch (err) {
          console.error(err);
      } finally {
          setIsLoading(false);
      }
  };

  useEffect(() => { 
      fetchUsers(); 
  }, [fetchUsers]);

  const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData(prev => ({ ...prev, [name]: value }));
  };

  return {
      users,
      formData,
      isLoading,
      error,
      handleChange,
      createUser,
      deleteUser,
      toggleStatus
  };
};