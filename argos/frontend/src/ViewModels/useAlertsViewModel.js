// src/ViewModels/useAlertsViewModel.js
import { useState, useEffect } from 'react';

// Endereço da API do backend
const API_URL = 'http://localhost:5000';

// Mapeamento de severidade para atender ao layout
const SEVERITY_MAP = {
  "ATIVIDADE SUSPEITA DETECTADA DO IP": "CRÍTICA",
  "EVENTO CATEGORIZADO COMO SUSPEITO": "ALTA"
};

const getSeverity = (motivo) => {
    // CORREÇÃO: Itera sobre o mapa de severidades para encontrar uma correspondência
    for (const key in SEVERITY_MAP) {
        if (motivo.toUpperCase().includes(key)) {
            return SEVERITY_MAP[key];
        }
    }
    return 'BAIXA'; // Retorna uma severidade padrão caso não encontre
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

        // Transforma os dados da API para o formato esperado pelo componente da View
        const formattedAlerts = data.map(alert => ({
            // CORREÇÃO: Utiliza o ID único fornecido pelo backend
            id: alert.id, 
            // CORREÇÃO: Usa o campo 'motivo' em vez de 'reason'
            ruleName: alert.motivo.split(':')[0], 
            timestamp: new Date(alert['@timestamp']).toLocaleString('pt-BR'),
            activityType: alert.motivo,
            severity: getSeverity(alert.motivo)
        }));

        setAlerts(formattedAlerts);

    } catch (error) {
        console.error("Erro ao buscar alertas:", error);
        setAlerts([]); // Limpa os alertas em caso de erro
    } finally {
        setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    // Atualiza a cada 30 segundos para manter a lista de alertas recente
    const intervalId = setInterval(fetchAlerts, 30000);
    return () => clearInterval(intervalId);
  }, []);

  return {
    alerts,
    isLoading,
  };
};