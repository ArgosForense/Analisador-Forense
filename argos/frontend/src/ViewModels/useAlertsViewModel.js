import { useState, useEffect } from 'react';

const API_URL = 'http://localhost:5000';

const SEVERITY_MAP = {
  "ATIVIDADE SUSPEITA DETECTADA DO IP": "CRÍTICA",
  "EVENTO CATEGORIZADO COMO SUSPEITO": "ALTA"
};

const getSeverity = (motivo) => {
    for (const key in SEVERITY_MAP) {
        if (motivo.toUpperCase().includes(key)) {
            return SEVERITY_MAP[key];
        }
    }
    return 'BAIXA'; 
};


export const useAlertsViewModel = () => {
  const [alerts, setAlerts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchAlerts = async () => {
    setIsLoading(true);
    try {
        const response = await fetch(`${API_URL}/alertas`);
        if (!response.ok) {
            throw new Error('Falha ao buscar alertas da API');
        }
        const data = await response.json();

        const formattedAlerts = data.map(alert => ({
            id: alert.id, 
            ruleName: alert.motivo.split(':')[0], 
            timestamp: new Date(alert['@timestamp']).toLocaleString('pt-BR'),
            activityType: alert.motivo,
            severity: getSeverity(alert.motivo)
        }));

        setAlerts(formattedAlerts);

    } catch (error) {
        console.error("Erro ao buscar alertas:", error);
        setAlerts([]); 
    } finally {
        setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const intervalId = setInterval(fetchAlerts, 30000);
    return () => clearInterval(intervalId);
  }, []);

  return {
    alerts,
    isLoading,
  };
};