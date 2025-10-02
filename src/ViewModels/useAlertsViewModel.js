import { useState, useEffect } from 'react';

export const useAlertsViewModel = () => {
  const [alerts, setAlerts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchAlerts = async () => {
    setIsLoading(true);
    // Simulação de alertas ativos
    const mockAlerts = [
      { 
        id: 103, 
        ruleName: 'Acesso de IP Suspeito (RN09)', 
        timestamp: '2025-05-20 18:05:00', 
        activityType: 'Acesso detectado do IP suspeito Y.Y.Y.Y',
        severity: 'CRÍTICA' 
      },
      { 
        id: 101, 
        ruleName: 'Tentativa de Login Fora de Hora (RN07)', 
        timestamp: '2025-05-21 23:45:10', 
        activityType: 'Tentativa de acesso fora de hora',
        severity: 'ALTA'
      },
      { 
        id: 102, 
        ruleName: 'Múltiplas Falhas de Login (RN08)', 
        timestamp: '2025-05-21 11:30:22', 
        activityType: 'Múltiplas falhas de login para o usuário X',
        severity: 'MÉDIA' 
      },
    ];
    
    await new Promise(resolve => setTimeout(resolve, 500));
    setAlerts(mockAlerts);
    setIsLoading(false);
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  return {
    alerts,
    isLoading,
  };
};