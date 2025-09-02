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
    """
    Valida o token JWT recebido na requisição, garantindo que o usuário está autenticado.

    - Decodifica o token JWT usando a chave secreta e o algoritmo definidos.
    - Extrai o ID e o tipo (gestor ou usuário) do token.
    - Busca a entidade correspondente no banco de dados.
    - Retorna o objeto autenticado (Gestor ou Usuario) para uso nas rotas protegidas.
    - Lança exceção HTTP 401 em caso de token inválido, expirado ou gestor/usuário não encontrado.
    *Conclusão:* Pode ser usado para bloquear rotas de usuário/gesto não autenticados.
    """
    
    try:
        #Decodifica o token
        dicionario_informacoes = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id = int(dicionario_informacoes.get("sub"))
        tipo = dicionario_informacoes.get("tipo")
    except JWTError:
        #Erro na decodificação do token
        raise HTTPException(status_code=401, detail="Acesso Negado: Token inválido ou expirado")
    
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
    