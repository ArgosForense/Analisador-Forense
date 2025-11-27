import pytest
from app.core.security import gerar_hash_senha, verificar_senha

def test_funcionalidade_hash_senha():
    """
    Testa se o sistema gera hash corretamente e valida senhas.
    """
    # 1. Definir uma senha de teste
    senha_plana = "senha123"

    # 2. O teste solicita a função gerar_hash_senha
    hash_gerado = gerar_hash_senha(senha_plana)

    # VERIFICAÇÕES (ASSERTS):
    
    # O hash não pode ser igual à senha original (deve estar criptografado)
    assert hash_gerado != senha_plana
    
    # O hash deve ser uma string
    assert isinstance(hash_gerado, str)
    
    # O hash deve ser longo (padrão do bcrypt)
    assert len(hash_gerado) > 20

    # 3. O teste solicita verificar_senha com a senha CERTA
    verificacao_correta = verificar_senha(senha_plana, hash_gerado)
    assert verificacao_correta is True

    # 4. O teste solicita verificar_senha com a senha ERRADA
    verificacao_errada = verificar_senha("senhaErrada", hash_gerado)
    assert verificacao_errada is False