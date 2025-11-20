import React from 'react';
import { useLogDashboardViewModel } from '../../ViewModels/useLogDashboardViewModel'; 
import { LogTable } from './LogTable'; 

const StatCard = ({ title, value, colorClass, icon, description }) => (
  <div className={`p-5 bg-white dark:bg-gray-800 rounded-xl shadow-lg transition-all duration-300 transform hover:scale-[1.02] border-b-4 ${colorClass}`}>
    <div className="flex items-center">
      {/* Ícone com cor de fundo light/dark baseada na cor da borda */}
      <div className={`p-3 rounded-full ${colorClass.replace('border-b-4', '').replace('border-', 'bg-opacity-20 text-')}`}>
        {icon}
      </div>
      <div className="ml-4">
        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</p>
        <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{value}</p>
      </div>
    </div>
    <p className="text-xs mt-3 text-gray-500 dark:text-gray-400">{description}</p>
  </div>
);


export const LogDashboardScreen = () => {
  // Utiliza o ViewModel para buscar dados reais
  const { logs, isLoading, error, searchTerm, setSearchTerm, stats} = useLogDashboardViewModel();
  
  return (
    <div className="p-8 bg-white dark:bg-gray-800 rounded-lg shadow-xl mx-auto">
      <h2 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
          Dashboard de Análise de Logs (HU-13)
      </h2>
      
      {/* Barra de Pesquisa */}
      <div className="space-y-4 mb-8">
        <div className="relative">
          <input
            type="text"
            placeholder="Pesquisar logs por termo, IP ou fonte..."
            className="w-full p-3 pl-10 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            disabled={isLoading}
          />
          <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
      </div>

      {/* Cards de Estatísticas */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <StatCard title="Total de Logs" value={stats.totalLogs} colorClass="border-indigo-500" icon={<svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>} description="Últimos 30 segundos." />
        <StatCard title="Alertas" value={stats.warningCount} colorClass="border-yellow-500" icon={<svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>} description="Atenção requerida." />
        <StatCard title="Erros Críticos" value={stats.errorCount} colorClass="border-red-500" icon={<svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>} description="Falhas de sistema." />
        <StatCard title="Fontes Únicas" value={stats.uniqueIPs} colorClass="border-green-500" icon={<svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>} description="IPs distintos." />
      </div>

      {/* Tabela */}
      <div className="mt-8">
          <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Logs Recentes</h3>
          <LogTable logs={logs} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default LogDashboardScreen;