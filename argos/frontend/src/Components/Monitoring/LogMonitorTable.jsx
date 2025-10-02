import React from 'react';
import { useRealTimeLogViewModel } from '../../ViewModels/useRealTimeLogViewModel';

export const LogMonitorTable = () => {
  // O ViewModel agora retorna o termo de busca (searchTerm) e a função para atualizá-lo (setSearchTerm)
  const { logs, isLoading, searchTerm, setSearchTerm } = useRealTimeLogViewModel();

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'WARNING': return 'text-yellow-500';
      case 'CRITICAL': return 'text-red-600 font-bold';
      case 'INFO':
      default: return 'text-green-500';
    }
  };

  return (
    <div className="p-8 bg-white dark:bg-gray-800 rounded-lg shadow-xl mx-auto">
      <h3 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
        HU-13: Logs de Acesso em Tempo Real
      </h3>

      {/* ===== CAMPO DE PESQUISA ADICIONADO ===== */}
      <div className="mb-5">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Pesquisar por mensagem, IP, severidade..."
          className="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-shadow"
        />
      </div>

      {isLoading && <p className="text-indigo-500 mb-4">Atualizando logs...</p>}
      <div className="overflow-x-auto border rounded-lg dark:border-gray-700">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-300">Data/Hora</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-300">Fonte</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-300">Severidade</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-300">Mensagem do Evento</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-300">IP de Origem</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:divide-gray-700">
            {logs.length > 0 ? (
              logs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">{log.timestamp}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">{log.source}</td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm ${getSeverityColor(log.severity)}`}>{log.severity}</td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-gray-300 max-w-xs truncate">{log.message}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-300">{log.ip}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
                  Nenhum log de acesso encontrado.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};