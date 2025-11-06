import { useState, useEffect, useCallback, useMemo } from 'react';

// Endereço da API e Intervalo de Atualização (Ajuste se necessário)
const API_URL = 'http://localhost:5000';
const LOG_UPDATE_INTERVAL = 30000; // 30 segundos

/**
 * Determina a severidade do log com base em seus campos.
 * Adiciona 'ERROR' para logs mais críticos.
 * @param {object} log - Objeto de log retornado da API.
 * @returns {('ERROR'|'WARNING'|'INFO')}
 */
const getSeverity = (log) => {
  // Lógica de severidade
  if (log.categoria === 'suspeito' || log.evento === 'entrada_falhou' || log.mensagem?.toUpperCase().includes('SUSPEITO')) {
      return 'WARNING';
  }
  if (log.mensagem?.toUpperCase().includes('ERROR') || log.mensagem?.toUpperCase().includes('FALHA') || log.severity === 'ERROR') {
      return 'ERROR';
  }
  return 'INFO';
};

/**
 * Hook ViewModel para gerenciar o estado e a lógica do Dashboard de Logs.
 * Exportado para ser consumido pelo LogDashboardScreen.
 */
export const useLogDashboardViewModel = () => {
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState(null);

  // Função centralizada para buscar logs da API
  const fetchLogs = useCallback(async (query) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
      if (!response.ok) {
        throw new Error('Falha ao buscar dados da API. Status: ' + response.status);
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
    } catch (err) {
      console.error("Erro ao buscar logs:", err);
      setError('Não foi possível conectar ao serviço de logs. Verifique a API.');
      setLogs([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Efeito para debounce na busca (ao digitar)
  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      fetchLogs(searchTerm);
    }, 500);
    return () => clearTimeout(debounceTimer);
  }, [searchTerm, fetchLogs]);

  // Efeito para atualização periódica (tempo real)
  useEffect(() => {
    fetchLogs(searchTerm); // Busca inicial
    const intervalId = setInterval(() => {
      fetchLogs(searchTerm);
    }, LOG_UPDATE_INTERVAL);
    return () => clearInterval(intervalId);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  // Métrica 1: Cálculo de estatísticas agregadas (Memoizado para performance)
  const stats = useMemo(() => {
    const totalLogs = logs.length;
    const warningCount = logs.filter(log => log.severity === 'WARNING').length;
    const errorCount = logs.filter(log => log.severity === 'ERROR').length;
    // Garante que 'N/A' não conte como um IP único
    const uniqueIPs = new Set(logs.map(log => log.ip).filter(ip => ip !== 'N/A')).size;

    return {
      totalLogs,
      warningCount,
      errorCount,
      uniqueIPs,
    };
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