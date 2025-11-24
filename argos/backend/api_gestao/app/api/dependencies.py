from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from beanie import PydanticObjectId

from app.core.config import settings
from app.models.user_model import Usuario
from app.models.gestor_model import Gestor

# Token URL aponta para a rota de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# REMOVIDO: obter_sessao() -> Não é mais necessário com Beanie

async def verificar_token(token: str = Depends(oauth2_scheme)):
    """
    Valida o token JWT de forma Assíncrona.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        user_type: str = payload.get("tipo")
        
        if user_id is None or user_type is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Converte string para ObjectId se necessário (Beanie aceita string no get)
    # Buscas assíncronas no Mongo
    if user_type == "gestor":
        user = await Gestor.get(user_id)
        if not user:
            raise credentials_exception
        return user
        
    elif user_type == "usuario":
        user = await Usuario.get(user_id)
        if not user:
            raise credentials_exception
        if not user.is_ativo():
            raise HTTPException(status_code=400, detail="Usuário inativo")
        return user
        
    else:
        raise credentials_exception

async def nivel_acesso_gestor(usuario_logado = Depends(verificar_token)):
    """
    Garante que apenas Gestores acessem a rota.
    """
    if not isinstance(usuario_logado, Gestor):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acesso restrito a gestores"
        )
    return usuario_logado