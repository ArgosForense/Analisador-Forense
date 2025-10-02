import React from 'react';
import { useAlertsViewModel } from '../../ViewModels/useAlertsViewModel';

export const AlertsList = () => {
  const { alerts, isLoading } = useAlertsViewModel();

  const getSeverityBadge = (severity) => {
    const baseStyle = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium';
    switch (severity) {
      case 'CRÍTICA': return `${baseStyle} bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300`;
      case 'ALTA': return `${baseStyle} bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300`;
      case 'MÉDIA': return `${baseStyle} bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300`;
      case 'BAIXA': 
      default: return `${baseStyle} bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300`;
    }
  };

  return (
    <div className="p-8 bg-white dark:bg-gray-800 rounded-lg shadow-xl mx-auto">
      <h3 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
        Lista de Alertas de Atividades Suspeitas
      </h3>
      {isLoading && <p className="text-indigo-500 mb-4">Carregando alertas...</p>}
      
      <div className="space-y-4">
        {alerts.length > 0 ? (
          alerts.map((alert) => (
            <div key={alert.id} className="p-4 border border-gray-200 rounded-md dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <div className="flex justify-between items-start">
                <div className="flex flex-col">
                  <span className="text-lg font-medium text-gray-900 dark:text-white">{alert.activityType}</span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">Regra: {alert.ruleName}</span>
                  <span className="text-xs text-gray-400 dark:text-gray-500">Detectado em: {alert.timestamp}</span>
                </div>
                <div className={getSeverityBadge(alert.severity)}>
                  {alert.severity}
                </div>
              </div>
              <div className="mt-2 text-right">
                <a href={`/alerts/${alert.id}`} className="text-sm font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
                  Ver Detalhes »
                </a>
              </div>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-500 dark:text-gray-400">Nenhum alerta ativo encontrado.</p>
        )}
      </div>
    </div>
  );
};