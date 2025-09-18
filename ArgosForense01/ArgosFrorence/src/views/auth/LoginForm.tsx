import { useState } from "react";
import { LoginViewModel } from "../../viewmodels/LoginViewModel";

export default function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const viewModel = new LoginViewModel();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const success = await viewModel.signIn({ username, password });
    if (success) {
      alert("Login realizado com sucesso!");
    } else {
      alert(viewModel.error);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-sm mx-auto p-4 bg-gray-800 rounded"
    >
      <h2 className="text-xl font-bold mb-4">Login</h2>

      <input
        type="text"
        placeholder="Usuário"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="w-full p-2 mb-2 rounded bg-gray-700 text-white"
      />

      <input
        type="password"
        placeholder="Senha"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full p-2 mb-2 rounded bg-gray-700 text-white"
      />

      {viewModel.error && (
        <p className="text-red-500 mb-2">{viewModel.error}</p>
      )}

      <button
        type="submit"
        className="w-full p-2 bg-blue-600 rounded hover:bg-blue-500"
      >
        Entrar
      </button>
    </form>
  );
}

