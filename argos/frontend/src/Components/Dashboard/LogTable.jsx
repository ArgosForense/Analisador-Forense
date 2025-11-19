import React from 'react';

export const LogTable = ({ logs, isLoading }) => {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'ERROR': return 'text-red-600 font-bold dark:text-red-400';
      case 'WARNING': return 'text-yellow-600 font-medium dark:text-yellow-400';
      case 'INFO':
      default: return 'text-indigo-600 dark:text-indigo-400';
    }
  };

  return (
    <div className="overflow-x-auto border rounded-lg dark:border-gray-700 shadow-md">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead className="bg-gray-50 dark:bg-gray-700">
          <tr>
            {/* Títulos das colunas */}
            {['Hora', 'Severidade', 'Fonte', 'IP de Origem', 'Mensagem'].map(header => (
              <th
                key={header}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-300"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:divide-gray-700">
          {isLoading ? (
             <tr><td colSpan="5" className="py-8 text-center text-indigo-500 dark:text-indigo-400">Carregando logs em tempo real...</td></tr>
          ) : logs.length === 0 ? (
             <tr><td colSpan="5" className="py-8 text-center text-gray-500 dark:text-gray-400">Nenhum log encontrado para o termo de pesquisa.</td></tr>
          ) : (
            logs.slice(0, 15).map((log) => (
              <tr key={log.id} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                {/* Data/Hora: pega apenas a hora para economizar espaço */}
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {log.timestamp.split(', ')[1]}
                </td>
                {/* Severidade */}
                <td className={`px-6 py-4 whitespace-nowrap text-sm ${getSeverityColor(log.severity)}`}>
                  {log.severity}
                </td>
                {/* Fonte */}
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  {log.source}
                </td>
                {/* IP */}
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
                  {log.ip}
                </td>
                {/* Mensagem: truncada para caber */}
                <td className="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 max-w-xs truncate" title={log.message}>
                  {log.message}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
      {/* Rodapé da tabela com info de atualização */}
      <div className="p-3 text-xs text-right bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-400 rounded-b-lg">
          Atualização a cada 30 segundos. Exibindo os últimos {Math.min(logs.length, 15)} logs.
      </div>
    </div>
  );
};