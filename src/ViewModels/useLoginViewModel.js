import { useState, useCallback } from 'react';

const loginService = {
  authenticate: async (email, password) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (email === 'gestor@soc.com' && password === 'SenhaSegura123!') {
          resolve({ token: 'abc123token', user: { name: 'Gestor SOC', profile: 'Gestor de SOC' } });
        } else {
          reject(new Error('Credenciais inválidas.'));
        }
      }, 1000);
    });
  },
};

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
      setError('Por favor, preencha todos os campos.');
      setIsLoading(false);
      return;
    }

    try {
      const data = await loginService.authenticate(email, password);
      console.log('Login bem-sucedido!', data);
      // Lógica para armazenar token e redirecionar
    } catch (err) {
      setError(err.message || 'Erro ao tentar fazer login.');
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