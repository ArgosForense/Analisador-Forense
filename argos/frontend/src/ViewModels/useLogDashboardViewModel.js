import { useState, useEffect, useCallback, useMemo } from 'react';

const API_URL = 'http://localhost:5000';
const LOG_UPDATE_INTERVAL = 30000;

export const getSeverity = (log) => {
  if (log.categoria === 'suspeito' || log.evento === 'entrada_falhou' || log.mensagem?.toUpperCase().includes('SUSPEITO')) {
      return 'WARNING';
  }
  if (log.mensagem?.toUpperCase().includes('ERROR') || log.mensagem?.toUpperCase().includes('FALHA') || log.severity === 'ERROR') {
      return 'ERROR';
  }
  return 'INFO';
};

export const useLogDashboardViewModel = () => {
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState(null);

  const fetchLogs = useCallback(async (query) => {
    setIsLoading(true);
    // Não limpamos o erro imediatamente aqui para evitar "flicker" se for um refresh automático
    
    try {
      const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
      
      if (!response.ok) {
        throw new Error(`Erro ${response.status}: Serviço de logs indisponível.`);
      }
      
      const data = await response.json();

      const formattedLogs = data.map(log => ({
        id: log.id || crypto.randomUUID(),
        timestamp: new Date(log['@timestamp'] || Date.now()).toLocaleString('pt-BR'),
        source: log.nome || 'N/A',
        message: log.mensagem || log.message || 'Mensagem Indisponível',
        severity: getSeverity(log),
        ip: log.ip_origem || 'N/A'
      }));

      setLogs(formattedLogs);
      setError(null); // Sucesso, limpa erros anteriores

    } catch (err) {
      console.error("Falha ao buscar logs:", err);
      
      // Tratamento específico para servidor desligado (Connection Refused)
      if (err.message.includes('Failed to fetch')) {
          setError('O servidor de Logs (Porta 5000) parece estar desligado. Inicie o backend Flask.');
      } else {
          setError(err.message || 'Erro desconhecido ao buscar logs.');
      }
      
      // Mantém os logs antigos se houver, ou limpa se preferir
      // setLogs([]); 
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
      if (!error) { // Só tenta atualizar automaticamente se não estiver com erro crítico de conexão
          fetchLogs(searchTerm);
      }
    }, LOG_UPDATE_INTERVAL);
    return () => clearInterval(intervalId);
  }, [searchTerm, fetchLogs, error]); // Adicionado error nas dependências

  const stats = useMemo(() => {
    const totalLogs = logs.length;
    const warningCount = logs.filter(log => log.severity === 'WARNING').length;
    const errorCount = logs.filter(log => log.severity === 'ERROR').length;
    const uniqueIPs = new Set(logs.map(log => log.ip).filter(ip => ip !== 'N/A')).size;

    return { totalLogs, warningCount, errorCount, uniqueIPs };
  }, [logs]);

  const topSources = useMemo(() => {
      const sourceCounts = logs.reduce((acc, log) => {
          acc[log.source] = (acc[log.source] || 0) + 1;
          return acc;
      }, {});

      return Object.entries(sourceCounts)
          .sort(([, countA], [, countB]) => countB - countA)
          .slice(0, 5)
          .map(([source, count]) => ({ source, count }));
  }, [logs]);

  return {
    logs,
    isLoading,
    error,
    searchTerm,
    setSearchTerm,
    stats,
    topSources,
  };
};