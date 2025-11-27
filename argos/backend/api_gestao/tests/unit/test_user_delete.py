import pytest
from unittest.mock import patch, AsyncMock
from app.services.user_service import UserService
from beanie import PydanticObjectId

@pytest.mark.asyncio
async def test_deletar_usuario_existente():
    """
    Cenário: O teste solicita deletar um usuário existente.
    Objetivo: Verificar se o método .delete() é chamado no objeto do usuário.
    """
    
    # --- 1. ARRANGE (Preparação) ---
    
    user_id_teste = PydanticObjectId()
    
    # O objeto 'usuario' deve ser um AsyncMock para que seus métodos (como .delete)
    # também sejam assíncronos automaticamente.
    usuario_mock = AsyncMock()
    
    with patch("app.services.user_service.user_repository") as mock_repo:
               
        mock_repo.get = AsyncMock(return_value=usuario_mock)
        
        service = UserService()
        
        # --- 2. ACT (Ação) ---
        await service.deletar_usuario(user_id_teste)
        
        # --- 3. ASSERT (Verificação) ---
        
        # Verifica se o serviço buscou o usuário
        mock_repo.get.assert_called_once_with(user_id_teste)
        
        # Verifica se o método .delete() foi chamado na instância do usuário
        usuario_mock.delete.assert_called_once()
        
        print("\n✅ Teste Passou: Deleção do usuário validada com sucesso!")