// argos/frontend/src/ViewModels/useLogDashboardViewModel.test.js
import { describe, it, expect } from 'vitest';
import { getSeverity } from './useLogDashboardViewModel';

describe('Lógica de Severidade (getSeverity)', () => {
  
  // Cenário 1: Categoria "suspeito"
  it('deve retornar WARNING quando a categoria for "suspeito"', () => {
    const logEntrada = { 
      categoria: 'suspeito', 
      mensagem: 'Acesso normal',
      evento: 'login'
    };
    
    const resultado = getSeverity(logEntrada);
    
    expect(resultado).toBe('WARNING');
  });

  // Cenário 2: Mensagem normal (Login efetuado)
  it('deve retornar INFO para mensagem "Login efetuado" (sem indícios de erro)', () => {
    const logEntrada = { 
      categoria: 'autenticacao', 
      mensagem: 'Login efetuado',
      evento: 'login_sucesso'
    };
    
    const resultado = getSeverity(logEntrada);
    
    expect(resultado).toBe('INFO');
  });

  // Teste Extra (Opcional): Verifica se ERROR funciona
  it('deve retornar ERROR quando a mensagem contém "FALHA"', () => {
    const logEntrada = { mensagem: 'FALHA DE CONEXÃO' };
    expect(getSeverity(logEntrada)).toBe('ERROR');
  });
});