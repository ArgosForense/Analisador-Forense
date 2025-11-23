import { useState, useCallback } from 'react';
import { useAuthStatus } from './useAuthStatus';

const API_BASE_URL = 'http://localhost:8000';

const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const useNewUserViewModel = () => {
  const { getAuthHeaders } = useAuthStatus();
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    profileId: '',
  });
  
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
 
  

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Limpa o erro específico do campo quando o usuário digita
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  }, [errors]); // 'errors' é dependência pois é lido dentro

  
  const validate = useCallback(() => {
    let newErrors = {};
    if (!formData.name) newErrors.name = 'Nome é obrigatório.';
    
    if (!formData.email) {
      newErrors.email = 'E-mail é obrigatório.';
    } else if (!isValidEmail(formData.email)) {
      newErrors.email = 'Formato de e-mail inválido.';
    }
    
    if (!formData.profileId) newErrors.profileId = 'Perfil é obrigatório.'; //(HU-8)

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [formData]); 

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    
    if (!validate()) return;

    setIsLoading(true);
    try {
      const payload = {
          nome: formData.name,
          email: formData.email,
          perfil_id: parseInt(formData.profileId)
      };

      const response = await fetch(`${API_BASE_URL}/usuarios/`, {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify(payload)
      });

      if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Erro ao criar usuário.');
      }

      alert(`Usuário ${formData.name} adicionado com sucesso! Credenciais enviadas por e-mail.`);
      
      setFormData({ name: '', email: '', profileId: '' });

    } catch (apiError) {
      setErrors(prev => ({ ...prev, general: apiError.message }));
    } finally {
      setIsLoading(false);
    }
  // CORREÇÃO AQUI: Adicionamos 'validate' nas dependências
  }, [formData, getAuthHeaders, validate]); 

  return {
    formData,
    errors,
    isLoading,
    handleChange,
    handleSubmit,
  };
};