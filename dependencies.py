from models import db
from sqlalchemy.orm import sessionmaker
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