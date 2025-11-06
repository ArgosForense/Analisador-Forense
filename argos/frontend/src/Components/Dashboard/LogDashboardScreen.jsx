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
  const { logs, isLoading, error, searchTerm, setSearchTerm, stats, topSources } = useLogDashboardViewModel();
  
  return (
    <div className="p-8 bg-white dark:bg-gray-800 rounded-lg shadow-xl mx-auto">
      
      {/* Título Principal no Padrão (2xl, font-semibold, mb-6) */}
      <h2 className="text-2xl font-semibold mb-6 text-gray-900 dark:text-white">
          Dashboard de Análise de Logs (HU-13)
      </h2>
      
      {/* 1. Área de Filtros e Erros */}
      <div className="space-y-4 mb-8">
        <div className="relative">
          <input
            type="text"
            placeholder="Pesquisar logs por termo, IP ou fonte..."
            className="w-full p-3 pl-10 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-shadow"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            disabled={isLoading}
          />
          {/* Icone de Lupa */}
          <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-gray-500" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        </div>

        {error && (
            <div className="p-4 text-sm font-medium text-red-700 bg-red-100 rounded-md dark:bg-red-900 dark:text-red-300 flex items-center shadow-sm" role="alert">
              <svg className="h-5 w-5 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86 1.84 18a2 2 0 0 0 1.71 3h16.9a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
              <span className="font-bold">Atenção:</span> {error}
            </div>
          )}
      </div>


      {/* 2. Cartões de Estatísticas */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <StatCard
          title="Total de Logs"
          value={stats.totalLogs.toLocaleString('pt-BR')}
          colorClass="border-indigo-500"
          icon={<svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/><path d="M12 12v4"/><path d="M12 7v1"/></svg>}
          description="Contagem de logs da última janela de 30 segundos."
        />
        <StatCard
          title="Alertas (Warning)"
          value={stats.warningCount.toLocaleString('pt-BR')}
          colorClass="border-yellow-500"
          icon={<svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86 1.84 18a2 2 0 0 0 1.71 3h16.9a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>}
          description="Eventos que requerem atenção imediata."
        />
        <StatCard
          title="Erros Críticos"
          value={stats.errorCount.toLocaleString('pt-BR')}
          colorClass="border-red-500"
          icon={<svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>}
          description="Logs que indicam falhas de sistema (Severity: ERROR)."
        />
        <StatCard
          title="Fontes de IP Únicas"
          value={stats.uniqueIPs.toLocaleString('pt-BR')}
          colorClass="border-green-500"
          icon={<svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 12h-4"/><path d="M14 12h-4"/><path d="M2 12h4"/><path d="M8 8v8"/><path d="M16 8v8"/></svg>}
          description="Número de IPs distintos que geraram logs."
        />
      </div>

      {/* 3. Layout Principal (Top Fontes e Tabela) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Top Fontes de Log */}
        <div className="lg:col-span-1 p-6 bg-gray-50 dark:bg-gray-700 rounded-xl shadow-inner border border-gray-200 dark:border-gray-700">
          <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white flex items-center">
            <svg className="h-5 w-5 mr-2 text-indigo-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><path d="M14 2v6h6"/></svg>
            Top 5 Fontes de Log
          </h3>
          <ul className="divide-y divide-gray-300 dark:divide-gray-600">
            {topSources.length > 0 ? (
                topSources.map((source, index) => (
                    <li key={index} className="flex justify-between items-center py-3">
                        <span className="text-sm font-medium text-gray-700 dark:text-gray-300 truncate">{source.source}</span>
                        <span className="px-3 py-1 text-xs font-semibold rounded-full bg-indigo-200 text-indigo-900 dark:bg-indigo-900 dark:text-indigo-200">
                        {source.count}
                        </span>
                    </li>
                ))
            ) : (
                <li className="text-center text-gray-500 dark:text-gray-400 py-4 text-sm">Nenhuma fonte ativa.</li>
            )}
          </ul>
        </div>

        {/* Tabela de Logs em Tempo Real */}
        <div className="lg:col-span-2">
          {/* Título da tabela usando h3 para hierarquia interna */}
          <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Logs Recentes em Tempo Real</h3>
          <LogTable logs={logs} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
};

export default LogDashboardScreen;