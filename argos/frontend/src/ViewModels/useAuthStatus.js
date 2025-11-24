import { useState, useEffect } from 'react';

export const useAuthStatus = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(null);

  useEffect(() => {
    // MUDANÇA: Agora verificamos o sessionStorage (limpa ao fechar a aba)
    const storedToken = sessionStorage.getItem('access_token');
    if (storedToken) {
      setToken(storedToken);
      setIsAuthenticated(true);
    }
  }, []);

  const login = (accessToken) => {
    // MUDANÇA: Salva na sessão, não no disco
    sessionStorage.setItem('access_token', accessToken);
    setToken(accessToken);
    setIsAuthenticated(true);
  };

  const logout = () => {
    // MUDANÇA: Remove da sessão
    sessionStorage.removeItem('access_token');
    setToken(null);
    setIsAuthenticated(false);
  };

  // Função auxiliar para pegar o cabeçalho de autorização
  const getAuthHeaders = () => {
    // MUDANÇA: Lê da sessão
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.getItem('access_token')}`
    };
  };

  return { isAuthenticated, token, login, logout, getAuthHeaders };
};