from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oath2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Gestor, Usuario
from jose import jwt, JWTError

def pegar_sessao():
    """
    Função para abrir e fechar a conexão com o banco de dados, sempre fechando a sessão após o uso.
    """
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        # retorna o valor sem fechar a sessão
        yield session
    finally:
        session.close()
        
# Para ter acesso a uma rota deve estar obrigatoriamente autenticado - Sera usado como Bloqueio de Endpoints 
def verificar_token(token: str = Depends(oath2_schema), session: Session = Depends(pegar_sessao)):
    """_summary_
    """
    
    try:
        #Decodifica o token
        dicionario_informacoes = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id = int(dicionario_informacoes.get("sub"))
        tipo = dicionario_informacoes.get("tipo")
    except JWTError:
        #Erro na decodificação do token
        raise HTTPException(status_code=401, detail="Acesso Negado: Token inválido ou expirado")
    
    # Extrai o ID do gestor ou usuario do token
    # gestor = session.query(Gestor).filter(Gestor.id == id).first()
    # usuario = session.query(Usuario).filter(Usuario.id == id).first()
    # if not usuario and not gestor:
    #     raise HTTPException(status_code=401, detail="Acesso Inválido: Gestor ou Usuário não encontrado")
    # elif gestor:
    #     return gestor
    # else:
    #     return usuario
    if tipo == "gestor":
        gestor = session.query(Gestor).filter(Gestor.id == id).first()
        if not gestor:
            raise HTTPException(status_code=401, detail="Acesso Inválido: Gestor não encontrado")
        return gestor
    elif tipo == "usuario":
        usuario = session.query(Usuario).filter(Usuario.id == id).first()
        if not usuario:
            raise HTTPException(status_code=401, detail="Acesso Inválido: Usuário não encontrado")
        return usuario
    else:
        raise HTTPException(status_code=401, detail="Tipo de usuário inválido no token")
    