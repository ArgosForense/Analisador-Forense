// src/ViewModels/useRealTimeLogViewModel.js

import { useState, useEffect, useCallback } from 'react';
// import { mockLogs } from '../Models/logs'; // <-- Remova esta linha

// Dados do Model (logs simulados) adicionados aqui temporariamente:
const mockLogs = [
    { id: 1, timestamp: '2025-05-21 10:00:00', source: 'Firewall-01', message: 'Connection established', severity: 'INFO', ip: '192.168.1.10' },
    { id: 2, timestamp: '2025-05-21 10:05:00', source: 'Server-Web', message: 'User "admin" logged in successfully', severity: 'INFO', ip: '203.0.113.45' },
    { id: 3, timestamp: '2025-05-21 10:10:00', source: 'DB-Prod', message: 'Query latency high', severity: 'WARNING', ip: '10.0.0.5' },
];

// Intervalo de atualização de 5 minutos (300000 ms) conforme requisito
const LOG_UPDATE_INTERVAL = 300000; 

export const useRealTimeLogViewModel = () => {
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchLogs = useCallback(async () => {
    setIsLoading(true);
    try {
      // Simulação de adição de um novo log a cada fetch (para simular tempo real)
      const newLogEntry = { 
        id: Date.now(), 
        timestamp: new Date().toISOString().slice(0, 19).replace('T', ' '), 
        source: 'Endpoint-A', 
        message: 'Acesso normal ao diretório de logs.', 
        severity: 'INFO',
        ip: '172.16.0.1' 
      };
      
      // Adiciona o novo log ao topo e garante que os mocks estejam presentes
      setLogs(prevLogs => [newLogEntry, ...mockLogs.slice(0, 5), ...prevLogs].slice(0, 50)); 
    } catch (error) {
      console.error("Erro ao buscar logs:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLogs(); // Busca inicial
    
    // Configura o intervalo de atualização (HU-13)
    const intervalId = setInterval(fetchLogs, LOG_UPDATE_INTERVAL);

    // Limpeza do intervalo ao desmontar
    return () => clearInterval(intervalId);
  }, [fetchLogs]);

  return {
    logs,
    isLoading,
  };
};