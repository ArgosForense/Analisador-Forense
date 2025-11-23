import { useState, useEffect, useCallback } from 'react';
import { useAuthStatus } from './useAuthStatus';

const API_BASE_URL = 'http://localhost:8000';

export const useProfileViewModel = () => {
    // 1. Obtenha a função getAuthHeaders do hook de autenticação
    const { getAuthHeaders } = useAuthStatus(); 
    
    const [profiles, setProfiles] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    // 2. CORREÇÃO: fetchProfiles deve ser estável.
    const fetchProfiles = useCallback(async () => {
        setIsLoading(true);
        try {
            // Chama a função getAuthHeaders() diretamente na hora da execução
            const headers = getAuthHeaders(); 
            
            const response = await fetch(`${API_BASE_URL}/perfis/`, {
                headers: headers
            });
            
            if (response.ok) {
                const data = await response.json();
                // Para evitar loops, só atualize se os dados forem realmente diferentes (opcional, mas boa prática)
                setProfiles(data);
            }
        } catch (err) {
            console.error("Erro ao buscar perfis:", err);
            setError("Falha ao carregar perfis.");
        } finally {
            setIsLoading(false);
        }
        // 3. O PULO DO GATO: Remova 'getAuthHeaders' das dependências se ela não for memoizada no hook de origem.
        // Se 'useAuthStatus' cria uma nova função 'getAuthHeaders' a cada render, isso causa o loop.
        // Vamos deixar o array vazio [] para garantir que a função fetchProfiles seja criada apenas UMA VEZ.
        // (O ESLint pode reclamar, mas neste caso é necessário para quebrar o loop se o hook anterior não for otimizado)
        
    }, []); 

    // Inicializar lista
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

            // Verifica erros antes de tentar ler o JSON
            if (!response.ok) {
                // Tenta ler o erro, mas se falhar (ex: erro de rede), usa mensagem genérica
                let errorMessage = 'Erro ao deletar perfil';
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || errorMessage;
                } catch { 
                    // Se não for JSON válido, ignora
                }
                throw new Error(errorMessage);
            }

            // SUCESSO! (Não tentamos ler response.json() aqui pois é um DELETE 204 vazio)
            
            // Atualiza a lista localmente
            setProfiles(prev => prev.filter(p => p.id !== id));
            alert("Perfil excluído com sucesso!");

        } catch (err) {
            console.error("Erro no delete:", err);
            alert(`Erro: ${err.message}`);
        } finally {
            setIsLoading(false);
        }
    };

    return {
        profiles,
        isLoading,
        error,
        createProfile,
        deleteProfile
    };
};