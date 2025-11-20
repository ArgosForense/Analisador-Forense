import React from 'react';
import { useLoginViewModel } from '../../ViewModels/useLoginViewModel';
// Removemos useNavigate e useAuthStatus daqui, pois o App.jsx vai cuidar do redirecionamento

export const LoginScreen = ({ onLoginSuccess }) => {
  const {
    email,
    setEmail,
    password,
    setPassword,
    isLoading,
    error,
    handleLogin: vmHandleLogin
  } = useLoginViewModel();

  const onSubmit = async (e) => {
      try {
          const accessToken = await vmHandleLogin(e);
          
          if (accessToken) {
            // Ao chamar isso, o App.jsx atualiza o estado 'isAuthenticated' para true.
            // O componente <PublicRoute> no App.jsx detectará a mudança e fará o redirecionamento.
            onLoginSuccess(accessToken); 
          }

      } catch (err) {
          console.error("Erro no login:", err);
      }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="max-w-md w-full p-6 space-y-8 bg-white rounded-xl shadow-lg dark:bg-gray-800">
        <h2 className="text-center text-3xl font-extrabold text-gray-900 dark:text-white">
          Analisador Argos
        </h2>
        <form className="mt-8 space-y-6" onSubmit={onSubmit}>
            {error && (
            <div className="p-3 text-sm text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800" role="alert">
              {error}
            </div>
            )}
          
            <div className="rounded-md shadow-sm -space-y-px">
                <div>
                <label htmlFor="email-address" className="sr-only">E-mail</label>
                <input
                    id="email-address"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                    placeholder="Endereço de E-mail"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    disabled={isLoading}
                />
                </div>
                <div>
                <label htmlFor="password" className="sr-only">Senha</label>
                <input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                    className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                    placeholder="Senha"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={isLoading}
                />
                </div>
            </div>

            <div>
                <button
                type="submit"
                disabled={isLoading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:bg-indigo-500 dark:hover:bg-indigo-600 disabled:opacity-50"
                >
                {isLoading ? 'Autenticando...' : 'Entrar'}
                </button>
            </div>
        </form>
      </div>
    </div>
  );
};