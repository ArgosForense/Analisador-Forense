import { useState } from 'react';

export const useAuthStatus = () => {
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