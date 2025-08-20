from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

# Criação da conexão com o banco de dados
db = create_engine("sqlite:///banco_test.db")

# Cria a base para criação dos modelos
Base = declarative_base()

# criar as classes/tabelas do banco de dados
# 1.TipoUsuario
class Usuario(Base):
    __tablename__ = "usuarios"
    
    #TIPOS_USUARIOS = (
    #    ("ADMIN", "Administrador"),
    #    ("USER", "Usuário Comum"),
    #    ("...", "..."),
    #)
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    tipo_usuario = Column("tipo_usuario") # quais são????????????
    ativo = Column("ativo", Boolean)
    
    def __init__(self, nome, email, senha, tipo_usuario="USER", ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo_usuario = tipo_usuario
        self.ativo = ativo
# 

# executa a criação dos metadados do banco (criação efetiva do banco)
