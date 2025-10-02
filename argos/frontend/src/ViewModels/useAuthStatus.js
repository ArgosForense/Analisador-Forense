import { useState } from 'react';

export const useAuthStatus = () => {
  // Simula o estado de autenticação. Em uma aplicação real, isso checaria um token JWT.
  const [isAuthenticated, setIsAuthenticated] = useState(
      localStorage.getItem('isAuth') === 'true'
  );

  const login = () => {
    localStorage.setItem('isAuth', 'true');
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('isAuth');
    setIsAuthenticated(false);
  };

  return { isAuthenticated, login, logout };
};