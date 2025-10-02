import { useState, useCallback } from 'react';
//import { mockProfiles } from '../Models/logs';
// Adicione a definição do Model (simulada) diretamente aqui para evitar o erro de path:
const mockProfiles = [
  { id: 1, name: 'Gestor de SOC' },
  { id: 2, name: 'Analista de Segurança Nível 1' },
  { id: 3, name: 'Especialista Forense' },
];


const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const useNewUserViewModel = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    profileId: '',
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const profiles = mockProfiles;

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  }, [errors]);

  const validate = () => {
    let newErrors = {};
    if (!formData.name) newErrors.name = 'Nome é obrigatório.';
    if (!formData.email) {
      newErrors.email = 'E-mail é obrigatório.';
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = 'Formato de e-mail inválido.';
    }
    if (!formData.profileId) newErrors.profileId = 'Perfil é obrigatório (HU-8/RN02).';

    // Simulação de "Usuário existente" (Critério 2)
    if (formData.email === 'user@existente.com') {
      newErrors.email = 'Usuário já existe no sistema.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    try {
      console.log('Dados a serem enviados:', formData);
      await new Promise(resolve => setTimeout(resolve, 1500));
      alert(`Usuário ${formData.name} adicionado com sucesso!`);
      // Limpar formulário se necessário
    } catch (apiError) {
      setErrors(prev => ({ ...prev, general: 'Erro ao incluir usuário.' }));
    } finally {
      setIsLoading(false);
    }
  }, [formData]);

  return {
    formData,
    errors,
    profiles,
    isLoading,
    handleChange,
    handleSubmit,
  };
};