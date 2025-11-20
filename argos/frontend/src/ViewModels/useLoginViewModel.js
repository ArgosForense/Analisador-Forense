import { useState, useCallback } from 'react';

// URL do FastAPI (Gestão)
const API_BASE_URL = 'http://localhost:8000'; 

export const useLoginViewModel = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleLogin = useCallback(async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    if (!email || !password) {
      const msg = 'Por favor, preencha todos os campos.';
      setError(msg);
      setIsLoading(false);
      // Retornamos uma Promise rejeitada para o componente saber que falhou
      throw new Error(msg);
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // O Backend espera "email" e "senha" (conforme LoginSchema)
        body: JSON.stringify({ email: email, senha: password }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Tratamento específico para Erros de Validação do FastAPI (422)
        if (response.status === 422 && data.detail) {
            // O FastAPI retorna uma lista de erros em 'detail'
            const validationErrors = Array.isArray(data.detail) 
                ? data.detail.map(err => `${err.loc[1]}: ${err.msg}`).join(' | ')
                : data.detail;
            throw new Error(`Erro de Validação: ${validationErrors}`);
        }
        
        // Erros de negócio (400 - Credenciais inválidas, etc)
        throw new Error(data.detail || 'Falha na autenticação.');
      }

      // Sucesso: Retorna o token
      return data.access_token;

    } catch (err) {
      console.error("Login Error Details:", err);
      setError(err.message || 'Erro ao tentar fazer login.');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [email, password]);

  return {
    email,
    setEmail,
    password,
    setPassword,
    isLoading,
    error,
    handleLogin,
  };
};