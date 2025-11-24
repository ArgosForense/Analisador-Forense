import { useState, useEffect, useCallback } from 'react';
import { useAuthStatus } from './useAuthStatus';

const API_BASE_URL = 'http://localhost:8000';

export const useProfileViewModel = () => {
    const { getAuthHeaders } = useAuthStatus();
    
    const [profiles, setProfiles] = useState([]);
    const [permissions, setPermissions] = useState([]); // Novo estado para permissões
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchProfiles = useCallback(async () => {
        setIsLoading(true);
        try {
            const headers = getAuthHeaders();
            
            // Busca Perfis
            const resProfiles = await fetch(`${API_BASE_URL}/perfis/`, { headers });
            if (resProfiles.ok) {
                const data = await resProfiles.json();
                setProfiles(data.map(p => ({...p, id: p.id || p._id})));
            }

            // Busca Permissões (NOVO - Para preencher os checkboxes corretamente)
            const resPerms = await fetch(`${API_BASE_URL}/permissoes/`, { headers });
            if (resPerms.ok) {
                const dataP = await resPerms.json();
                setPermissions(dataP.map(p => ({...p, id: p.id || p._id})));
            }

        } catch (err) {
            console.error("Erro ao buscar dados:", err);
            setError("Falha ao carregar perfis/permissões.");
        } finally {
            setIsLoading(false);
        }
    }, []); 

    useEffect(() => {
        fetchProfiles();
    }, [fetchProfiles]);

    const createProfile = async (nome, permissoesIds) => {
        setIsLoading(true);
        setError(null);
        try {
            const payload = { nome, permissoes_ids: permissoesIds };
            const response = await fetch(`${API_BASE_URL}/perfis/`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Erro ao criar perfil');
            }

            await fetchProfiles(); 
            return true; 
        } catch (err) {
            setError(err.message);
            return false;
        } finally {
            setIsLoading(false);
        }
    };

    const deleteProfile = async (id) => {
        if (!window.confirm("Tem certeza que deseja excluir este perfil?")) return;

        setIsLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/perfis/${id}`, {
                method: 'DELETE',
                headers: getAuthHeaders()
            });

            if (!response.ok) {
                // Tenta ler erro, se falhar usa genérico
                let msg = 'Erro ao deletar';
                try {
                    const errObj = await response.json();
                    if (errObj && errObj.detail) msg = errObj.detail;
                } catch (e) {
                    // Não foi possível parsear o corpo de erro; mantém mensagem genérica
                    console.warn('Falha ao ler corpo de erro:', e);
                }
                throw new Error(msg);
            }

            setProfiles(prev => prev.filter(p => p.id !== id));
            alert("Perfil excluído com sucesso!");

        } catch (err) {
            alert(`Erro: ${err.message}`);
        } finally {
            setIsLoading(false);
        }
    };

    return {
        profiles,
        permissions, 
        isLoading,
        error,
        createProfile,
        deleteProfile
    };
};