// Simula a estrutura e alguns dados iniciais para logs
export const mockLogs = [
    { id: 1, timestamp: '2025-05-21 10:00:00', source: 'Firewall-01', message: 'Connection established', severity: 'INFO', ip: '192.168.1.10' },
    { id: 2, timestamp: '2025-05-21 10:05:00', source: 'Server-Web', message: 'User "admin" logged in successfully', severity: 'INFO', ip: '203.0.113.45' },
    { id: 3, timestamp: '2025-05-21 10:10:00', source: 'DB-Prod', message: 'Query latency high', severity: 'WARNING', ip: '10.0.0.5' },
];

export const mockProfiles = [
    { id: 1, name: 'Gestor de SOC' },
    { id: 2, name: 'Analista de Segurança Nível 1' },
    { id: 3, name: 'Especialista Forense' },
];