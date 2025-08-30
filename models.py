from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

# Criação da conexão com o banco de dados
db = create_engine("sqlite:///banco_test.db")

# Cria a base para criação dos modelos
Base = declarative_base()

# criar as classes/tabelas do banco de dados
# Empresa possui gestores, estes cadastram usuários e cada usuário é atribuido a um perfil com permissões definidas pelo gestor
# 1.TipoUsuario

 

class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    cnpj = Column("cnpj", String, nullable=False)
    gestores = Column("gestores", String) # lista de gestores vinculados a empresa
    
    def __init__(self, nome, cnpj, gestores):
        self.nome = nome
        self.cnpj = cnpj
        self.gestores = gestores
        
class gestor(Base):
    __tablename__ = "gestores"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    empresa_id = Column("empresa_id", Integer, ForeignKey("empresas.id"))
    
    def __init__(self, nome, email, senha, empresa_id):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.empresa_id = empresa_id
        
        
class Usuario(Base):
    __tablename__ = "usuarios"
    
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    empresa_id = Column("empresa_id", Integer, ForeignKey("empresas.id"))
    
    def __init__(self, nome, email, senha, ativo=True, empresa_id=None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.empresa_id = empresa_id
        
class Perfil(Base):
    __tablename__ = "perfis"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    permissoes = Column("permissoes", String) # lista de permissões vinculadas ao perfil
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"))
    
    def __init__(self, nome, permissoes, usuario_id):
        self.nome = nome
        self.permissoes = permissoes
        self.usuario_id = usuario_id
# executa a criação dos metadados do banco (criação efetiva do banco)
