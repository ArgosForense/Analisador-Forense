// src/ViewModels/useRealTimeLogViewModel.js

import { useState, useEffect, useCallback } from 'react';

const API_URL = 'http://localhost:5000';
const LOG_UPDATE_INTERVAL = 300000; // 5 minutos

const getSeverity = (log) => {
  if (log.categoria === 'suspeito') return 'WARNING';
  if (log.evento === 'entrada_falhou') return 'WARNING';
  if (log.mensagem?.toUpperCase().includes('SUSPEITO')) return 'WARNING';
  if (log.evento === 'entrada_efetuada') return 'INFO';
  return 'INFO';
};

export const useRealTimeLogViewModel = () => {
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchLogs = useCallback(async (query) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
      if (!response.ok) {
        throw new Error('Falha ao buscar dados da API');
      }
      const data = await response.json();

      const formattedLogs = data.map(log => ({
        id: log.id,
        timestamp: new Date(log['@timestamp']).toLocaleString('pt-BR'),
        source: log.nome || 'N/A',
        message: log.mensagem,
        severity: getSeverity(log),
        ip: log.ip_origem || 'N/A'
      }));

      setLogs(formattedLogs);
    } catch (error) {
      console.error("Erro ao buscar logs:", error);
      setLogs([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      fetchLogs(searchTerm);
    }, 500);
    return () => clearTimeout(debounceTimer);
  }, [searchTerm, fetchLogs]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetchLogs(searchTerm);
    }, LOG_UPDATE_INTERVAL);
    return () => clearInterval(intervalId);
  }, [searchTerm, fetchLogs]);

  return {
    logs,
    isLoading,
    searchTerm,
    setSearchTerm,
  };
};