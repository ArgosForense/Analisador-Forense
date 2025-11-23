from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.database import SessionLocal
from app.core.config import settings
from app.models.user_model import Usuario
from app.models.gestor_model import Gestor

# A URL do token agora aponta para a nova rota de login no auth_router # (tokenUrl="/auth/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-form")

def obter_sessao():
    """
    Função para abrir e fechar a conexão com o banco de dados, 
    sempre fechando a sessão após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def verificar_token(token: str = Depends(oauth2_scheme), db: Session = Depends(obter_sessao)):
    """
    Valida o token JWT recebido na requisição, garantindo que o usuário está autenticado.

    - Decodifica o token JWT usando a chave secreta e o algoritmo definidos.
    - Extrai o ID e o tipo (gestor ou usuário) do token.
    - Busca a entidade correspondente no banco de dados.
    - Retorna o objeto autenticado (Gestor ou Usuario) para uso nas rotas protegidas.
    - Lança exceção HTTP 401 em caso de token inválido, expirado ou gestor/usuário não encontrado.
    *Conclusão:* Pode ser usado para bloquear rotas de usuário/gestor não autenticados.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        user_type: str = payload.get("tipo")
        if user_id is None or user_type is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acesso Negado: Token inválido ou expirado")
    
    if user_type == "gestor":
        user = db.query(Gestor).filter(Gestor.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acesso Inválido: Gestor não encontrado")
        return user
    elif user_type == "usuario":
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user or not user.is_ativo():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acesso Inválido: Usuário não encontrado ou desativado")
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tipo de usuário inválido no token")
    
def nivel_acesso_gestor(usuario_logado = Depends(verificar_token)):
    """
    Dependência que garante que apenas gestores autenticados podem acessar a rota.
    """
    if not isinstance(usuario_logado, Gestor):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada. Apenas gestores podem acessar esta rota")
    return usuario_logado