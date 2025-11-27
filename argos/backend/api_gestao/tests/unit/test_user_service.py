import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreateSchema
from app.models.gestor_model import Gestor

# Usamos mark.asyncio pois o método a ser testado é async
@pytest.mark.asyncio
async def test_criar_usuario_gera_email_correto():
    """
    Testa se o UserService gera o e-mail institucional corretamente
    e salva o usuário sem bater no banco real.
    """
    
    # --- 1. ARRANGE (Preparação) ---
    
    # Dados de entrada
    user_in = UserCreateSchema(
        nome="João Silva",
        email="joao.pessoal@gmail.com",
        perfil_id="65f1a2b3c4d5e6f7a8b9c0d1" # ID fictício
    )
    
    # Gestor fictício (apenas para passar como argumento)
    gestor_mock = MagicMock(spec=Gestor)
    gestor_mock.id = "507f1f77bcf86cd799439011"

    # --- MOCKING (A Mágica) ---
    
    # A. Mockamos o Repositório para dizer que "não existe usuário com esse email"
    with patch("app.services.user_service.user_repository") as mock_repo:
        # Quando o service perguntar se o email existe, responda None (não existe)
        mock_repo.get_by_email = AsyncMock(return_value=None)

        # B. Mockamos a função de gerar email para garantir o valor esperado
        # (Isso isola o teste da lógica interna do security.py)
        with patch("app.services.user_service.gerar_email_institucional") as mock_email_gen:
            mock_email_gen.return_value = "joao.silva@argos.com"

            # C. Mockamos a classe Usuario e sua instância
            with patch("app.services.user_service.Usuario") as MockUsuarioClass:
                # Criamos uma instância falsa que será retornada pelo construtor
                usuario_instance_mock = AsyncMock()
                MockUsuarioClass.return_value = usuario_instance_mock
                
                # Instancia o serviço
                service = UserService()

                # --- 2. ACT (Ação) ---
                resultado = await service.criar_usuario(user_in, gestor_mock)

                # --- 3. ASSERT (Verificação) ---

                # Verifica se o gerador de email foi chamado com o nome certo
                mock_email_gen.assert_called_once_with("João Silva")

                # Verifica se o objeto Usuario foi instanciado com o email gerado internamente
                # (Aqui validamos a Regra de Negócio!)
                _, kwargs = MockUsuarioClass.call_args
                assert kwargs["email"] == "joao.silva@argos.com"
                assert kwargs["nome"] == "João Silva"

                # Verifica se o método .create() foi chamado na instância (simulando o salvamento no banco)
                usuario_instance_mock.create.assert_called_once()

                # Verifica se o fetch_all_links (para carregar o perfil) foi chamado
                usuario_instance_mock.fetch_all_links.assert_called_once()
                
                print("\n✅ Teste Passou: Usuário criado com email 'joao.silva@argos.com'!")